Vending Machine API Documentation

API URL - http://localhost:5000/machine

1. To enlist all the available products
    Method -> GET
    Endpoint -> /products
    Payload -> None
    Response -> {
        "data": [
            {
            "product_currency": "INR",
            "product_id": 1,
            "product_name": "Lays",
            "product_price": 20,
            "product_quantity": 9,
            "product_url": "https://www.wallpapersdsc.net/wp-content/uploads/2016/09/Lays-Wallpaper.jpg"
            },
            {
            "product_currency": "INR",
            "product_id": 2,
            "product_name": "Kurkure",
            "product_price": 25,
            "product_quantity": 3,
            "product_url": "https://i.pinimg.com/originals/7f/9d/f0/7f9df0f4a662a01dd079989795b72e61.jpg"
            },
            .
            .
            .
        ],
        "success": true
    }

2. To login as admin
    Method -> POST
    Endpoint -> /user
    Payload -> {
        "password": 'admin'
    }
    Response -> {
        "data": [],
        "success": true
    }
    Here the password for the admin is set is 'admin'.

   
   Note: In requests # 3, 4, & 5, I have used an Authorisation header which is base64 encode of 'test:admin' to verify after I have successfully logged in as admin and can access the related endpoints.

3. To update a product stock
    Method -> PUT
    Endpoint -> /products
    Headers -> {
        Authorisation: dGVzdDphZG1pbg==
    }
    Payload -> {
        "product_id": 1,
        "product_quantity": 10
    }
    Response -> {
        "data": {
            "product_id": 1,
            "product_quantity": 10
        },
        "success": true
    }

4. To collect cash from the machine
    Method -> GET
    Endpoint -> /collect
    Headers -> {
        Authorisation: dGVzdDphZG1pbg==
    }
    Payload -> None
    Response -> {
        "data": {
            "amount": 0
        },
        "success": true
    }

5. To see the transaction history
    Method -> GET
    Endpoint -> /transactions
    Headers -> {
        Authorisation: dGVzdDphZG1pbg==
    }
    Payload -> None
    Response -> {
        "data": [
            {
            "amount": 20,
            "product_id": null,
            "product_quantity": null,
            "timestamp": "Wed, 01 Jul 2020 16:12:02 GMT",
            "transaction_id": 22,
            "transaction_name": "Collect cash",
            "type": "Withdraw"
            },
            {
            "amount": 20,
            "product_id": 1,
            "product_quantity": 1,
            "timestamp": "Wed, 01 Jul 2020 16:11:57 GMT",
            "transaction_id": 21,
            "transaction_name": "Buy Product",
            "type": "Buy"
            },
            .
            .
            .
        ],
        "success": true
    }

6. To buy a product
    This endpoint is a bit trivial to understand. Using session to achieve the behaviour of inserting notes in a vending machine and can successfully get your product or you can terminate your current request.

    Suppose I am buying Lays of Rs. 20
    A) Inserting Rs. 10 Note
        Method -> POST
        Endpoint -> /buy
        Payload -> {
            product_id: 1,
            product_price: 20,
            note: 10
        }
        Response -> {
            "data": {
                "add_amount": 10, 
                "product_id": 1, 
                "product_price": 20
            }, 
            "final_buy": false, 
            "success": true
        }

        Here, in response I am required to add an amount of at least 10 to buy the product. Session helps in maintaing the track of inserted notes by an user.

    B) Inserting Rs. 50 Note
        Method -> POST
        Endpoint -> /buy
        Payload -> {
            product_id: 1,
            product_price: 20,
            note: 50
        }
        Response -> {
            "data": {
                "balance": 40, 
                "product_id": 1, 
                "product_price": 20
            }, 
            "final_buy": true, 
            "success": true
        }

        Here, in response, I receive a balance amount of Rs. 40 to return to user and I have successfully bought the product.


    C) Wrong note inserted
    Method -> POST
        Endpoint -> /buy
        Payload -> {
            product_id: 1,
            product_price: 20,
            note: 15
        }
        Response -> {
            "final_buy": false, 
            "msg": "Invalid note passed", 
            "success": false
        }

7. To delete the session of buying a product & refund
    Method -> DELETE
    Endpoint -> /buy
    Payload -> None
    Response -> {
        "success": true
    }

    It deletes the current session of the user and refunds the money if applicable.

