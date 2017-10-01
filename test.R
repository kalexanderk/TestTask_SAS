library("openxlsx")
df_initial <- read.xlsx("Data/payments.xlsx", sheet=1)
typeof(df_initial)
class(df_initial)

change_date <- function(x) as.Date(x ,origin='1960-01-01')
df <- data.frame(df_initial['lead_id'], lapply(df_initial['dt'], change_date), df_initial['amount'])
df['weekday'] <- format(df['dt'], "%A")
summary(df)

shift <- function(d, k) rbind( tail(d,k), head(d,-k), deparse.level = 0 )
df['id_shifted'] <- shift(df['lead_id'], 1)

coun<-0

find_days_not_returned<-function(df){
  df['days_not_returned']<-0
  for(i in 1:nrow(df)){
    if ((df[i, 'lead_id']==df[i, 'id_shifted']) & (df[i, 'amount']==0)){
      if ((df[i, 'weekday']=='Saturday') | (df[i, 'weekday']=='Sunday')) {
        df[i, 'days_not_returned']=coun
        }
      else{
        coun=coun+1
        df[i, 'days_not_returned']=coun 
        }
    }
  else if ((df[i, 'lead_id']!=df[i, 'id_shifted']) | (df[i, 'amount']>0)){
    if (df[i, 'amount'] != 0){
      coun=0
      df[i,'days_not_returned']=coun
      }
    if (df[i, 'amount'] == 0){
      coun=1
      df[i, 'days_not_returned']=coun
      }
  }
}
return(df)
}

df_t<-find_days_not_returned(df)
df_t$id_shifted=NULL
#df_t is the result
