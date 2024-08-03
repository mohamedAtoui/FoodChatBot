from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper  
import generic_helper
app = FastAPI()
inprogress_orders={}

@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id=generic_helper.extract_session_id(output_contexts[0]["name"])
    
    intent_dic={
        "track.order - context : ongoing-order":track_order,
        "order.add- context: ongoing-order":add_to_order,
        "order complete-context: ongoing-order":complete_order,
        "order.remove-context: ongoing-order":remove_order
    }
    
    return intent_dic[intent](parameters,session_id)

def remove_order(parameters:dict,session_id:str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText":"I'm having a trouble finding your order",
        })
    current_order=inprogress_orders[session_id]
    food_items=parameters["meals"]
    removed_items=[]
    no_such_item=[]
    for item in food_items:
        if item not in current_order:
            no_such_item.append(item)
        else:
            removed_items.append(item)
            del current_order[item]
    
    if len(removed_items)>0:
        fullfilment_text=f"Removed {",".join(removed_items)} from your order!"
    
    if len(no_such_item)>0:
        fullfilment_text=f"Your order does not have {",".join(no_such_item)}"
        
    if len(current_order.keys())==0:
        fullfilment_text+= "Your order is emprty"
    else:
        stritem=generic_helper.get_string_from_food_dic(current_order)
        fullfilment_text+=f"Here is what is left in your order : {stritem}"
        
    return JSONResponse(content={
        "fulfillmentText":fullfilment_text
    })
        
def save_to_db(order:dict):
    next_order_id=db_helper.get_next_order_id()
    
    for food_item,quant in order.items():
        rcode=db_helper.insert_order_item(
            food_item,
            quant,
            next_order_id
        )
        
        if rcode == -1:
            return -1 
    db_helper.insert_order_tracking(next_order_id,"in progress")
    return next_order_id
def complete_order(parameters:dict,session_id:str):
    if session_id not in inprogress_orders:
        fulfillment_text="I am having a trouble finding your order :("
    else:
        order=inprogress_orders[session_id]
        order_id=save_to_db(order)
        if order_id==-1:
            fulfillment_text="Sorry I couldn't find order"
        else:
            order_total=db_helper.get_total_order_price(order_id)
        fulfillment_text = (
            f"Awesome! We have placed your order. "
            f"Here is your order ID: #{order_id}. "
            f"Your order total is {order_total}DA which you can pay with a card."
        )
        del inprogress_orders[session_id]
        return JSONResponse(content={
            "fulfillmentText":fulfillment_text
        })
        

def add_to_order(parameters: dict,sessio_id:str):
    food_items = parameters["meals"]
    quantity=parameters["number"]
    if len(food_items)!=len(quantity):
        fulfillment_text="Sorry I didn't understand. Can you please specify food items and quantity"
    else:
        fulfillment_text=f"Recieved {food_items} and {quantity} in the backend"
        new_food_dic=dict(zip(food_items,quantity))
        if sessio_id in inprogress_orders.keys():
            inprogress_orders[sessio_id].update(new_food_dic)
        else:
            inprogress_orders[sessio_id]=new_food_dic
        print(inprogress_orders)
    fulfillment_text="So far you have oreded: "+generic_helper.get_string_from_food_dic(inprogress_orders[sessio_id])+ ",Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
    
def track_order(parameters: dict,session_id:str):
    order_id = parameters['number']
    print(order_id)
    order_status = db_helper.get_order_status(order_id)
    
    if order_status:
        fulfillment_text = f"The order status for order ID: {int(order_id)} is: {order_status}"
    else:
        fulfillment_text = f"No order found with the ID: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



