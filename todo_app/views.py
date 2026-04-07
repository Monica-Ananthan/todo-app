from urllib import request
from django.shortcuts import render, get_object_or_404
from .models import Task, Category
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Count, Case, When, Value, IntegerField
from datetime import date
from django.core.paginator import Paginator
from datetime import datetime

# Create your views here.
def test(request):
    return render(request, 'test.html')

def index(request):
    filter_type = request.GET.get("filter")
    category_id = request.GET.get("category")

    tasks = Task.objects.annotate(
        is_completed_order=Case(
            When(completed=True, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('is_completed_order', '-id')

    if filter_type == "active":
        tasks = tasks.filter(completed=False)
    elif filter_type == "completed":
        tasks = tasks.filter(completed=True)

    if category_id:
        tasks = tasks.filter(category_id=category_id)
    
    paginator = Paginator(tasks, 5) 
    page_number = request.GET.get("page")
    tasks = paginator.get_page(page_number)

    categories = Category.objects.all()
    categories = categories.annotate(
        task_count=Count('task')
    )

    if request.headers.get("HX-Request"):
        return render(request, "todo_app/partials/task_list.html", {
            "tasks": tasks,
            "today": date.today(),
            "filter": filter_type
        })

    return render(request, "todo_app/index.html", {
        "tasks": tasks,
        "categories": categories,
        "filter": filter_type,
        "today": date.today()
    })

def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        category_id = request.POST.get("category")
        due_date = request.POST.get("due_date")

        if title:
            task = Task.objects.create(
                title=title,
                category_id=category_id if category_id else None,
                due_date = request.POST.get("due_date")
            )

            task_html = render_to_string(
                "todo_app/partials/task_item.html",
                {"task": task}
            )

            categories = Category.objects.annotate(task_count=Count('task'))

            category_html = render_to_string(
                "todo_app/partials/category_list.html",
                {"categories": categories}
            )

            return HttpResponse(f"""
                {task_html}

                <div hx-swap-oob="innerHTML:#category-list">
                    {category_html}
                </div>
            """)

    return HttpResponse(status=400)

def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()

    categories = Category.objects.annotate(task_count=Count('task'))

    task_html = render_to_string(
        "todo_app/partials/task_item.html",
        {"task": task}
    )

    category_html = render_to_string(
        "todo_app/partials/category_list.html",
        {"categories": categories}
    )

    return HttpResponse(f"""
        {task_html}

        <div hx-swap-oob="innerHTML:#category-list">
            {category_html}
        </div>
    """)

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()

    categories = Category.objects.annotate(task_count=Count('task'))

    category_html = render_to_string(
        "todo_app/partials/category_list.html",
        {"categories": categories}
    )

    return HttpResponse(f"""
        <div hx-swap-oob="innerHTML:#category-list">
            {category_html}
        </div>
    """)

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")

        if title:
            task.title = title

        if "due_date" in request.POST:
            if due_date:
                task.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            else:
                task.due_date = None

        task.save()

    return render(
        request,
        "todo_app/partials/task_item.html",
        {"task": task, "today": date.today()}
    )

def add_category(request):
    if request.method == "POST":
        name = request.POST.get("new_category", "").strip()

        if not name:
            return HttpResponse("""
                <div id="category-error" hx-swap-oob="innerHTML" class="text-red-500 text-xs mt-1">
                    Category name is required
                </div>
            """)

        if Category.objects.filter(name__iexact=name).exists():
            return HttpResponse("""
                <div id="category-error" hx-swap-oob="innerHTML" class="text-red-500 text-xs mt-1">
                    Category already exists
                </div>
            """)

        new_category = Category.objects.create(name=name)
        categories = Category.objects.all()

        options_html = render_to_string(
            "todo_app/partials/category_options.html",
            {
                "categories": categories,
                "selected_id": new_category.id
            }
        )

        return HttpResponse(f"""
            <div id="category-select" hx-swap-oob="innerHTML">
                {options_html}
            </div>

            <div id="category-error" hx-swap-oob="innerHTML"></div>

            <div id="category-input-reset" hx-swap-oob="innerHTML"></div>
        """)
    
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()

    categories = Category.objects.all()

    category_html = render_to_string(
        "todo_app/partials/category_list.html",
        {"categories": categories}
    )

    options_html = render_to_string(
        "todo_app/partials/category_options.html",
        {"categories": categories}
    )


    return HttpResponse(f"""
        <div hx-swap-oob="innerHTML:#category-list">
            {category_html}
        </div>

        <template hx-swap-oob="innerHTML:#category-select">
            {options_html}
        </template>
    """)

def category_list_partial(request):
    categories = Category.objects.all()
    categories = Category.objects.annotate(
        task_count=Count('task')
    )

    return render(
        request,
        "todo_app/partials/category_list.html",
        {"categories": categories}
    )
