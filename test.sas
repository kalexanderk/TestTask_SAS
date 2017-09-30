libname test 'C:\workshop\test\Files';

proc import datafile = 'C:\workshop\test\Data\payments.xlsx'
DBMS = xlsx OUT = test.initial_data replace;
format dt DDMMYY10.;
run;


data test.result(drop=wkday_index);
set test.initial_data;
wkday_index=weekday(dt);
length weekday $ 10;
if wkday_index=1 then weekday="Sunday";
	else if wkday_index=2 then weekday="Monday";
	else if wkday_index=3 then weekday="Tuesday";
	else if wkday_index=4 then weekday="Wednesday";
	else if wkday_index=5 then weekday="Thursday";
	else if wkday_index=6 then weekday="Friday";
	else if wkday_index=7 then weekday="Saturday";
run;