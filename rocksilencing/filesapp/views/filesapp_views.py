import json
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from filesapp.models.models import Design


def get_design(request, design_id):
    """Получает данные дизайна и обновляет сессию"""
    design = get_object_or_404(Design, pk=design_id)

    # Обновляем сессию
    request.session["design_id"] = str(design.id)
    request.session["design_name"] = design.name
    request.session["field"] = design.field
    request.session["cluster"] = design.cluster
    request.session["well"] = design.well
    request.session["calc_type"] = design.calc_type

    return JsonResponse({"status": "ok"})


def FilesMainWindow(request):
    """Отображает все Дизайны"""
    designs = Design.objects.all().order_by("-updated")

    # Очищаем сессию при заходе на страницу
    keys_to_clear = request.session.keys() - {
        "_auth_user_id",
        "_auth_user_backend",
        "_auth_user_hash",
    }
    for key in keys_to_clear:
        del request.session[key]

    return render(request, "designs/designs.html", {"designs": designs})


def create_design_view(request):
    """
    (Необязательная, старая версия). Создаёт новый дизайн через обычную POST-форму.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        field = request.POST.get("field")
        cluster = request.POST.get("cluster")
        well = request.POST.get("well")
        calc_type = request.POST.get("calc_type")

        if not name:
            messages.error(request, "Название дизайна не может быть пустым.")
            return redirect("filesapp:create_design")

        design = Design.objects.create(
            name=name, field=field, cluster=cluster, well=well, calc_type=calc_type
        )
        messages.success(request, f"Дизайн «{design.name}» успешно создан!")
        return redirect("filesapp:files_main_window")
    return render(request, "designs/create_design.html")


def edit_design_view(request, design_id):
    """
    Редактируем существующий дизайн.
    """
    design = get_object_or_404(Design, pk=design_id)
    if request.method == "POST":
        design.name = request.POST.get("name") or design.name
        design.field = request.POST.get("field") or design.field
        design.cluster = request.POST.get("cluster") or design.cluster
        design.well = request.POST.get("well") or design.well
        design.calc_type = request.POST.get("calc_type") or design.calc_type
        design.save()
        messages.success(request, f"Дизайн «{design.name}» успешно обновлён!")
        return redirect("filesapp:files_main_window")
    return render(request, "designs/edit_design.html", {"design": design})


def ajax_create_design(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            field = data.get("field", "").strip() or None
            cluster = data.get("cluster", "").strip() or None
            well = data.get("well", "").strip() or None
            calc_type = data.get("calc_type")

            if not name:
                return JsonResponse(
                    {"status": "error", "message": "Name is required"}, status=400
                )

            # Создаём дизайн
            design = Design.objects.create(
                name=name,
                field=field,
                cluster=cluster,
                well=well,
                calc_type=calc_type,
            )

            # Запоминаем в сессии
            request.session["design_id"] = str(design.id)
            request.session["design_name"] = design.name
            request.session["field"] = design.field
            request.session["cluster"] = design.cluster
            request.session["well"] = design.well
            request.session["calc_type"] = design.calc_type

            # Можно очистить какие-то специфические ключи, если нужно
            # keys_to_clear = ["salt_session_context"]
            # for key in keys_to_clear:
            #     if key in request.session:
            #         del request.session[key]

            return JsonResponse({"status": "ok", "design_id": str(design.id)})

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, status=400
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


def get_fields_json(request):
    """
    Возвращает JSON со списком уникальных месторождений (field).
    Пример: {"fields": ["Месторождение-1", "Месторождение-2", ...]}
    """
    fields = Design.objects.values_list("field", flat=True).distinct()
    # Исключаем случаи, когда field=None или field=""
    fields = [f for f in fields if f]
    return JsonResponse({"fields": list(fields)})


def get_clusters_json(request):
    """
    Возвращает список уникальных "кустов" (cluster) для выбранного месторождения (field).
    Пример запроса: GET /files/get_clusters_json/?field=Месторождение-1
    Пример ответа: {"clusters": ["Куст-1", "Куст-2"]}
    """
    field = request.GET.get("field")
    if not field:
        return JsonResponse({"clusters": []})
    clusters = (
        Design.objects.filter(field=field).values_list("cluster", flat=True).distinct()
    )
    clusters = [c for c in clusters if c]
    return JsonResponse({"clusters": list(clusters)})


def get_wells_json(request):
    """
    Возвращает список уникальных "скважин" (well) для выбранных месторождения + куста.
    Пример: GET /files/get_wells_json/?field=Месторождение-1&cluster=Куст-2
    Ответ: {"wells": ["Скважина-1", "Скважина-25"]}
    """
    field = request.GET.get("field")
    cluster = request.GET.get("cluster")
    if not field or not cluster:
        return JsonResponse({"wells": []})
    wells = (
        Design.objects.filter(field=field, cluster=cluster)
        .values_list("well", flat=True)
        .distinct()
    )
    wells = [w for w in wells if w]
    return JsonResponse({"wells": list(wells)})


def delete_design(request, design_id):
    if request.method == "POST":
        design = get_object_or_404(Design, pk=design_id)
        design.delete()
        return JsonResponse({"status": "ok"})
    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )
