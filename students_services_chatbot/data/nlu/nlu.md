## intent:greet
- Hi
- Hello
- Hey there
- Hey, there
- Hi, there
- Hi, bot
- Hi friend
- Hello, friend
- What's up
- What's up bot
- Good morning
- Good evening
- Good afternoon

## intent:bye
- Goodbye
- bye
- Goodnight
- Good bye
- See you
- See ya
- bye bot
- bye friend
- See you later
- Gotta go
- I gotta go
- Catch you later
- Talk to you later

## intent:thanks
- Thanks
- Thank you
- Thank bot
- Thanks, bot
- Thanks, bro
- Thank you so much
- Thank for that
- Ok Thanks
- Cool, Thanks!
- Amazing, Thanks
- Perfect, Thank you
- Great, Thank you! 

## intent:affirm
- Yes
- Ok
- Yes, I do
- Do it
- Ok.
- Sure
- Yeah
- Yep
- Accept
- Awesome!
- Ok cool
- Yes please
- I accept
- Nice
- Perfect
- Yup
- I will
- I do
- Great
- Ok man
- Yes, please.

## intent:deny
- No
- Absolutely not
- Never
- I don't think so
- No way
- No sorry
- No, sorry
- Not for me
- No, please
- I don't accept
- Deny
- Decline
- I deny
- I decline
- I will not do it
- I can't
- Not really
- Not sure
- I don't
- I don't want to
- No thanks

## intent:ask_grade
- What is my grade?
- What is my mark?
- Show me my grade?
- Show me my mark?
- What is my [MAS101](subject)'s grade?
- What is my [MLN101](subject)'s final grade?
- What is my [DBW](subject)'s grade?
- What is my [PRX](subject)'s mark?
- What is my grade in [CSI](subject)?
- What is my grade in [PRO192](subject)?
- What is my mark in [DBI](subject)?
- What is my mark in [SSG101](subject)?
- What mark do I have in [Data Warehouse](subject) subject?
- What mark do I have in [HCI201](subject)?
- what mark do I have in [CEA](subject)?
- I want to see my [PRF192](subject)'s mark.
- I want to see my mark in [PRX](subject).
- I want to see my [MLN](subject)'s grade.
- I want to see my grade in [MAD](subject).
- I want to know my grade in [MAE](subject).
- I want to know my [NWC](subject)'s grade.
- My [PRF](subject)'s mark please?
- My [SSC](subject)'s grade?
- Show me my grade in [ITE](subject).
- Show me my [MLN](subject)'s grade.
- Show me my mark in [MAD](subject).
- Show me my [PRX](subject)'s mark.

## intent:move_class
- I want to move out class.
- I want to move class.
- I want to move out.
- I want to move out class to the morning class.
- I want to move out class [MAS](subject).
- I want to move out [PRX](subject) class.
- I want to move class [PRF192](subject).
- Move class for me.
- Move out class for me.
- Move out class [HCI](subject) for me please.
- Can you move out class [MLN](subject) for me.
- Can you move my class [DBI202](subject) to the afternoon class.
- Move out class.
- I want to change class to the morning.
- I want to change my [SSG](subject) class.
- I want to change my [Data Warehouse](subject) class.

## intent:suspend_subject
- I want to suspend my [MAD](subject) subject.
- I want to suspend the [PRO192](subject).
- I want to cancel the [PRX](subject) subject.
- Suspend the [mln](subject:MLN) for me.
- Suspend the [PRO192](subject) for me.
- Please suspend the [NWC](subject) subject for me.
- Cancel my [SSC](subject) subject.
- Cancel my [mae101](subject:MAE101) subject.
- Cancel the [SSG101](subject) subject.
- I don't want to study the [DBI](subject) subject.
- I don't want to study [MAS](subject).
- I don't want to study [PRF192](subject) subject.

## intent:suspend_semester
- I want to suspend my [next semester](date).
- I want to suspend [next semester](date).
- I want to suspend semester.
- I want to suspend [the Spring semester](date).
- I want to suspend [Summer semester](date).
- I want to cancel [the Fall semester](date).
- I want to cancel semester.
- Suspend [next semester](date) for me.
- Cancel [the next semester](date) for me.
- I don't want to study in [the next semester](date).
- I don't want to study in [the Spring semester](date).
- I don't wanna study [next semester](date).
- I don't wanna study in [Summer semester](date).
- I don't want to study in [the Summer](date) and [Fall semester](date).

## intent:enter_data
- [MAE101](subject)
- [HCI301](subject)
- It's [SWD](subject)
- Its [CSI101](subject)
- The subject is [DBI201](subject)
- Subject [DBW](subject)
- [Summer](date)
- [Fall](date)
- It's [Spring](date)
- Its [Summer](date)
- [Fall](date) semester
- The semester is [Spring](date)

## synonym:USA
- usa
- U.S.A
- Usa
- u.s.a

## lookup:semester
- Spring
- Summer
- Fall

## regex:SUBJECT
- [a-zA-Z]{3}[0-9]{3}
