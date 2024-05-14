var stripe = Stripe('{{settings.STRIPE_PUBLIC_KEY}}');
var elements = stripe.elements();
var cardElement = elements.create('card');
cardElement.mount('#card-element');
var cardNumberElement = document.querySelector('#card-element .CardNumberElement');
var cardExpiryElement = document.querySelector('#card-element .CardExpiryElement');
var cardCvcElement = document.querySelector('#card-element .CardCvcElement');
var form = document.getElementById('payment-form');
var submitButton = document.getElementById('submit-button');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    submitButton.disabled = true;

    stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
    }).then(function(result) {
        if (result.error) {
            // Display payment errors to the user
            var errorElement = document.getElementById('payment-errors');
            errorElement.textContent = result.error.message;
            submitButton.disabled = false;
        } else {
            // Submit form with payment method details to server
            stripeTokenHandler(result.paymentMethod.id);
        }
    });
});

function stripeTokenHandler(paymentMethodId) {
    // Insert the payment method ID into the form
    var form = document.getElementById('payment-form');
    var hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'payment_method_id');
    hiddenInput.setAttribute('value', paymentMethodId);
    form.appendChild(hiddenInput);
    // Submit the form
    form.submit();
}
function handlePaymentResponse(response) {
    if (response.success) {
        // Payment successful
        document.getElementById('payment-response').innerHTML = "Payment successful!";
    } else if (response.error) {
        // Payment failed
        document.getElementById('payment-response').innerHTML = "Payment failed: " + response.error;
    }
}

