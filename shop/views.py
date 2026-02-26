from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.services.subdomains import assign_subdomain_to_user, check_subdomain_availability
from .forms import ProductForm, UserShopForm
from .models import Product, UserShop


ProductInlineFormSet = inlineformset_factory(
    UserShop,
    Product,
    form=ProductForm,
    extra=1,
    can_delete=True,
)


def _get_product_limit_for_user(user):
    plans = set(user.plan.values_list("value", flat=True))
    if "Pro" in plans:
        return 30
    if "Basic" in plans:
        return 15
    return 5


def shop_view(request, shop_id):
    shop = get_object_or_404(UserShop.objects.select_related("user"), id=shop_id, is_active=True)
    products_qs = shop.products.filter(is_active=True).order_by("-created_at")
    paginator = Paginator(products_qs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "shop/shop_view.html",
        {
            "shop": shop,
            "products": page_obj.object_list,
            "page_obj": page_obj,
        },
    )


@login_required
@require_POST
def create_shop_view(request):
    user_plan_values = set(request.user.plan.values_list("value", flat=True))
    has_paid_plan = "Basic" in user_plan_values or "Pro" in user_plan_values
    shop_count = UserShop.objects.filter(user=request.user).count()

    # Free users can create only one shop. More shops require Basic/Pro.
    if shop_count >= 1 and not has_paid_plan:
        messages.error(
            request,
            "پلن رایگان فقط اجازه ساخت یک سایت فروشگاهی را دارد. برای سایت بیشتر پلن پایه یا پرو تهیه کنید.",
        )
        return redirect("dashboard")

    requested_subdomain = (request.POST.get("subdomain") or "").strip().lower()
    has_existing_subdomain = hasattr(request.user, "subdomain")

    if not requested_subdomain and not has_existing_subdomain:
        messages.error(request, "برای ساخت سایت، وارد کردن ساب‌دامین الزامی است.")
        return redirect("dashboard")

    if requested_subdomain:
        check = check_subdomain_availability(requested_subdomain, user=request.user)
        if not check.available:
            messages.error(request, f"ساب‌دامین معتبر نیست: {check.reason}")
            return redirect("dashboard")

    form = UserShopForm(request.POST, request.FILES)
    if form.is_valid():
        shop = form.save(commit=False)
        shop.user = request.user
        shop.save()
        if requested_subdomain:
            assign_subdomain_to_user(request.user, requested_subdomain)
        messages.success(request, "فروشگاه شما با موفقیت ساخته شد.")
        return redirect("shop_manage", shop_id=shop.id)

    messages.error(request, "فرم ایجاد فروشگاه معتبر نیست. لطفا دوباره بررسی کنید.")
    return redirect("dashboard")


@login_required
def manage_shop_view(request, shop_id):
    shop = get_object_or_404(
        UserShop.objects.prefetch_related("products"),
        id=shop_id,
        user=request.user,
    )
    product_limit = _get_product_limit_for_user(request.user)

    if request.method == "POST":
        requested_subdomain = (request.POST.get("subdomain") or "").strip().lower()
        shop_form = UserShopForm(request.POST, request.FILES, instance=shop)
        formset = ProductInlineFormSet(request.POST, request.FILES, instance=shop, prefix="products")
        if shop_form.is_valid() and formset.is_valid():
            if requested_subdomain:
                check = check_subdomain_availability(requested_subdomain, user=request.user)
                if not check.available:
                    messages.error(request, f"ساب‌دامین معتبر نیست: {check.reason}")
                    return render(
                        request,
                        "shop/shop_manage.html",
                        {
                            "shop": shop,
                            "shop_form": shop_form,
                            "formset": formset,
                            "product_limit": product_limit,
                            "current_subdomain": getattr(getattr(request.user, "subdomain", None), "subdomain", ""),
                            "current_product_count": shop.products.count(),
                        },
                    )

            resulting_count = 0
            for form in formset.forms:
                cleaned = getattr(form, "cleaned_data", None) or {}
                if not cleaned or cleaned.get("DELETE"):
                    continue
                if form.instance.pk or cleaned.get("name"):
                    resulting_count += 1

            if resulting_count > product_limit:
                messages.error(
                    request,
                    f"سقف محصولات پلن شما {product_limit} عدد است. برای افزایش ظرفیت، پلن بالاتر تهیه کنید.",
                )
                return render(
                    request,
                    "shop/shop_manage.html",
                    {
                        "shop": shop,
                        "shop_form": shop_form,
                        "formset": formset,
                        "product_limit": product_limit,
                        "current_subdomain": getattr(getattr(request.user, "subdomain", None), "subdomain", ""),
                        "current_product_count": resulting_count,
                    },
                )

            shop_form.save()
            formset.save()
            if requested_subdomain:
                assign_subdomain_to_user(request.user, requested_subdomain)
            messages.success(request, "فروشگاه و محصولات با موفقیت ذخیره شدند.")
            return redirect("shop_manage", shop_id=shop.id)
        messages.error(request, "خطا در ثبت اطلاعات. فیلدها را بررسی کنید.")
    else:
        shop_form = UserShopForm(instance=shop)
        formset = ProductInlineFormSet(instance=shop, prefix="products")

    return render(
        request,
        "shop/shop_manage.html",
        {
            "shop": shop,
            "shop_form": shop_form,
            "formset": formset,
            "product_limit": product_limit,
            "current_subdomain": getattr(getattr(request.user, "subdomain", None), "subdomain", ""),
            "current_product_count": shop.products.count(),
        },
    )


@login_required
@require_POST
def delete_shop_view(request, shop_id):
    shop = get_object_or_404(UserShop, id=shop_id, user=request.user)
    shop.delete()
    messages.success(request, "فروشگاه حذف شد.")
    return redirect("dashboard")
