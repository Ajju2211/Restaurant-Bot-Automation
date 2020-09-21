

## order food path
*greet
    -utter_greet
*order_food
    -action_show_menu
	-order_form
	-form{"name":"order_form"}
	-form{"name":null}


    
## complaint path
*greet
    -utter_greet
*query_init
    -utter_query_type    
*complaint_init
	-complain_form
	-form{"name":"complain_form"}
	-form{"name":null}
	
	
## feedback path
*greet
	-utter_greet
*query_init
    -utter_query_type	
*feedback_init
	-feedback_form
	-form{"name":"feedback_form"}
	-form{"name":null}	

## faq path
*greet
	-utter_greet
*faq_init
    -faq_form
	-form{"name":"faq_form"}
	-form{"name":null}	




## feedback path with back in queries
*greet
	-utter_greet
*query_init
    -utter_query_type
*greetback
	- action_greet_back
	





	
<!--
## feedback path
*greet
	- utter_greet
*query_init
    utter_query_init	
*feedback_init
	-feedback_form
	-form{"name":"feedback_form"}
	-form{"name":null}

 ## path 1
* order_foodf
	- info_form
	- form{"name": "info_form"}
	- form{"name":null}
	- order_form
	- form{"name":"order_form"}
	- form{"name":null}
* goodbye
	- utter_goodbye 
## complain path
*complaint_init
    -utter_confirm_complain 
*affirm
    -complain_form
    -form{"name":"complain_form"}
    -form{"name":"null"}
    -utter_complain_values
*affirm  
    -utter_goodbye 
    
## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
-->