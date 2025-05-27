def calculate_final_price(discount_percent, original_price):
    '''
    calculate the final_price after applying discount

    Args:
        discount_percent (float): The discount percentage (e.g., 20 for 20%).
        original_price (float): The original price before the discount.

    Returns:
        float: The final price after the discount is applied.
    '''
    discount = (discount_percent / 100) * original_price
    final_price = original_price - discount
    return final_price
