libname test 'C:\workshop\test\Files';

proc import datafile = 'C:\workshop\test\Data\payments.xlsx'
DBMS = xlsx OUT = test.initial_data replace;
format dt DDMMYY10.;
run;

data test.result(drop=wkday_index coun);
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
by lead_id;
if first.lead_id and amount ne 0 then coun=0;
else if first.lead_id and amount=0 then coun=1;
if lead_id=lag(lead_id) and amount=0 then do;
    if wkday_index=1 or wkday_index=7 then days_not_returned=coun;
	if wkday_index ne 1 and wkday_index ne 7 then do;
		coun=coun+1;
		days_not_returned=coun;
	end;
end;
else if lead_id ne lag(lead_id) or amount>0 then do;
	if amount ne 0 then coun=0;
	if amount=0 then coun=1;
	days_not_returned=coun;
end;
retain coun;
run;

proc export 
  data=test.result 
  dbms=xlsx 
  outfile="c:\workshop\test\Files\result.xlsx" 
  replace;
run;
 
