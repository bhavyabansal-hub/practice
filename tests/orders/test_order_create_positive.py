# test_order_create_positive.py placeholder
def test_create_order_positive(sb_session):
    sb_session.open_url("/orders/create")
    sb_session.type_text("input[name='consignee']", "John Doe")
    sb_session.type_text("input[name='weight']", "5")
    sb_session.click("button#create-order")
    sb_session.assert_element_visible(".order-row")
