## intent:greet

- hey
- hello
- hi
- good morning
- good evening
- hey there

## intent:order_food

- I want to place an order.
- Hey bot help me to place an order.
- Hey bot can you help me to place order.
- Help me out to place order.
- Place order.
- I want to order.
- What all can i order?
- Place an order.
- Place an order for me.
- Help me to place order.

## intent: inform

- [Noodles](dish_name)
- [Burger](dish_name)
- [Pizza](dish_name)
- [Chicken](dish_name)
- [Sandwich](dish_name)
- [Poha](dish_name)
- [Samosa](dish_name)
- [Ice Cream](dish_name)
- My name is [Aditya Aggarwal](username)
- My name is [Pratik Banka](username)
- My name is [Gaurav Garg](username)
- My name is [Tejaswini](username)
- My name is [Awais Akhtar](username)
- My name is [Kshitij Anand](username)
- My name is [Muzzafar](username)
- My name is [Matloob Faruki](username)
- My name is [Satyam Jha](username)
- [7999545121](phone_number)
- [8464646451](phone_number)
- [8484645482](phone_number)
- [7984844848](phone_number)
- [7896421188](phone_number)
- [6486531484](phone_number)
- [4684615846](phone_number)
- [9446316548](phone_number)
- [4984415654](phone_number)
- [8444448489](phone_number)
- [8646153166](phone_number)
- [6456546656](phone_number)
- [6513215313](phone_number)
- [9864464645](phone_number)
- [2948613377](phone_number)
- [5593965741](phone_number)
- [back2](phone_number)
- [srffnwvb@aol.com](mailid)
- [kfquzxgm@zohocorp.com](mailid)
- [kpmvchemistryt@gmx.com](mailid)
- [vnalhydp@gmx.com](mailid)
- [xcpudvti@icloud.com](mailid)
- [icsplitf@gmx.com](mailid)
- [ymaegatr@zohocorp.com](mailid)
- [horstnrg@yahoo.com](mailid)
- [ffcmdyuv@gmail.com](mailid)
- [bkvnoija@gmail.com](mailid)
- [vrbgftmm@icloud.com](mailid)
- [brpdmaev@gmx.com](mailid)
- [back1](mailid)
- [yes](continue)
- [yes](continue) sure
- [Yes](continue) sure
- [Yes](continue)
- [YES](continue)
- [YES](continue) sure
- [NO](continue)
- [no](continue)
- [No](continue)
<!-- this is added -->
- [AB-123](customer_id)
- [BB-321](customer_id)
- [ABC-1234](product_id)
- [BBB-4321](product_id)
- [12345](transaction_id)
- [23232](transaction_id)
- [aZghg21@1hj](any_text)
- [azhar@jhj](any_text)

## regex:customer_id
- \b[A-Z]{2}-\d{3}\b
## regex:product_id
- \b[A-Z]{3}-\d{4}\b
## regex:transaction_id
- \b\d{5}\b
## regex:any_thing
- @sys.any

## regex:quantity
- \b\d{1,3}\b



## intent:goodbye

- bye
- goodbye
- see you around
- see you later

## intent:affirm

- [yes](confirm)
- [indeed](confirm)
- [of course](confirm)
- that sounds good
- [correct](confirm)

## intent:deny

- no
- never
- I don't think so
- don't like that
- no way
- not really

## intent:bot_challenge

- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?


## intent:complaint_init

-I want to complain
-I have a complain
-I have an issue
-I have a problem
-I want to report an problem
-I want to report an complain
-I want to report an isssue
-complain
-I am very angry with the service.

## intent:complain

- lots of fruits and vegetables
- too many snacks
- too many sweets
- too much junk food
- a lot of carbs
- too much fatty food
- very bad taste
- bad taste
- taste not good
- very spicy
- unhygenic packing
- dirty packing
- [very slow delivery]{"entity": "any_thing", "role": "complaint_input"}
- [the app does not respond at all]{"entity": "any_thing", "role": "complaint_input"}
- my discount coupon did not apply
- [Food Quality](complain_type)
- [Delivery](complain_type)
- [Naaniz App](complain_type)
- [Other](complain_type)

## intent:feedback_init

-i want to give feedback
-I want to give feedback
-where to give feedback
-wat to give feedback
-I have a feedback
-I have an issue
-I have a feedback
-I want to report an feedback
-feedback


## intent:question
-[what is naaniz?](question)
-[how to complain?](question)
-[how to pay?](question)
-[where is naaniz located?](question)


## intent:faq_init

-i want to ask faq
-I want to ask faq
-where to ask faq
-wat to ask faq
-I have a faq
-I have an question
-I have a faq
-I want to report an faq
-faq

## intent:rating
-[1](rating)
-[2](rating)
-[3](rating)
-[4](rating)
-[5](rating)

## intent:faq_choice
-[1](faq_choice)
-[2](faq_choice)
-[3](faq_choice)
-[4](faq_choice)
-[5](faq_choice)

## intent:query_init

-I want to query
-I have a query
-I have an issue
-I want to report an query
-I want to report queries
-query