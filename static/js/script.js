document.addEventListener("DOMContentLoaded", function () {
    const toastElList = [].slice.call(document.querySelectorAll('.toast'))
    toastElList.map(function (toastEl) {
    const toast = new bootstrap.Toast(toastEl, {
        delay: 4000,  // 4 seconds
        autohide: true
    });
    toast.show();
    });
});

document.addEventListener('DOMContentLoaded', () => {
  const checkbox = document.getElementById('id_same_as_shipping');

  if (checkbox) {
    checkbox.addEventListener('change', () => {
      const isChecked = checkbox.checked;

      const shippingAddress = document.getElementById('id_shipping_address');
      const shippingCity = document.getElementById('id_shipping_city');
      const shippingPostcode = document.getElementById('id_shipping_postcode');

      const billingAddress = document.getElementById('id_billing_address');
      const billingCity = document.getElementById('id_billing_city');
      const billingPostcode = document.getElementById('id_billing_postcode');

      if (isChecked) {
        billingAddress.value = shippingAddress.value;
        billingCity.value = shippingCity.value;
        billingPostcode.value = shippingPostcode.value;
      } else {
        billingAddress.value = '';
        billingCity.value = '';
        billingPostcode.value = '';
      }
    });
  }
});
