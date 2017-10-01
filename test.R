library("openxlsx")
df_initial <- read.xlsx("Data/payments.xlsx", sheet=1)
typeof(df_initial)
class(df_initial)

change_date <- function(x) as.Date(x ,origin='1960-01-01')
df <- data.frame(df_initial['lead_id'], lapply(df_initial['dt'], change_date), df_initial['amount'])
df['weekday'] <- format(df['dt'], "%A")
summary(df)

