## greet
* greet
    - utter_greet
    
## bye
* bye
    - utter_bye

## thanks
* thanks
    - utter_no_worries
    - utter_anything_else

## ask grade, don't give subject
* ask_grade
    - utter_ask_subject
* enter_data{"subject": "MAE101"}
    - action_store_subject
    - action_get_grade

## ask grade, already give subject
* ask_grade{"subject": "MAE101"}
    - action_store_subject
    - action_get_grade

## suspend subject, don't give subject
* suspend_subject
    - utter_ask_subject
* enter_data{"subject": "MAE101"}
    - action_store_subject
    - utter_confirm_suspend_subject
* affirm
    - action_suspend_subject

## suspend subject, already give subject
* suspend_subject{"subject": "MAE101"}
    - action_store_subject
    - utter_confirm_suspend_subject
* affirm
    - action_suspend_subject

## cancel while suspending subject, already give subject
* suspend_subject{"subject": "MAE101"}
    - action_store_subject
    - utter_confirm_suspend_subject
* deny
    - utter_ok
    - utter_anything_else
    
## cancel while suspending subject, don't give subject
* suspend_subject
    - utter_ask_subject
* enter_data{"subject": "MAE101"}
    - action_store_subject
    - utter_confirm_suspend_subject
* deny
    - utter_ok
    - utter_anything_else
