from django.shortcuts import render
import requests

def get_currency_data():
    """ Fetch currency data from the API """
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url)
        response.raise_for_status()
        currency_data = response.json()
        return currency_data
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues)
        print(f"Error fetching currency data: {e}")
        return None
    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON response: {e}")
        return None

def index(request):
    currency_to = "USD"
    result = None

    if request.method == "POST":
        # Get data from the HTML form
        try:
            amount = float(request.POST.get('amount'))
            currency_from = request.POST.get("currency_from")
            currency_to = request.POST.get("currency_to")
        except (ValueError, TypeError):
            # Handle invalid input gracefully
            result = "Invalid input"
        else:
            # Get currency exchange rates
            url = f"https://open.er-api.com/v6/latest/{currency_from}"
            try:
                response_data = requests.get(url).json()
                if "result" in response_data and response_data["result"] == "success":
                    rates = response_data.get("rates", {})
                    ex_target = rates.get(currency_to)
                    if ex_target is not None:
                        # Calculate the currency conversion
                        result = "{:.2f}".format(ex_target * amount)
                    else:
                        result = "Currency not found"
                else:
                    result = "Error fetching exchange rates"
            except requests.exceptions.RequestException as e:
                # Handle API request errors
                result = f"API request failed: {e}"

    context = {
        "result": result,
        "currency_to": currency_to,
        "currency_data": get_currency_data()
    }

    return render(request, "index.html", context)
