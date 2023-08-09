def categoricalData():
    while True:
        data_category = input(f"what category best describes your data: \ 1. Nature \ 2. People \ 3. Furniture \ 4. Food \ 5. Animals \ 6. Tools \ 7. Electronics \ 8. Art \ 9. Clothing \ 10. Other") # Broad
        if(data_category == '1'):
            Nature()
        elif(data_category == '2'):
            People()
        elif(data_category == '3'):
            Furniture()
        elif(data_category == '4'):
            Food()
        elif(data_category == '5'):
            Animals()
        elif(data_category == '6'):
            Tools()
        elif(data_category == '7'):
            Electronics()
        elif(data_category == '8'):
            Art()
        elif(data_category == '9'):
            Clothing()
        elif(data_category == '10'):  
            Other()
        # then verify that it is between 1 and 10

        # narrow down

        # 
