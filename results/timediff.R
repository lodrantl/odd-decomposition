library(tidyverse)
Sys.setlocale(category = "LC_ALL", locale = "Slovenian")

graphs <- read_csv(
  "timed.csv",
  col_types = cols(
    .default = col_integer(),
    percentage = col_double(),
    time = col_double(),
    avgtime = col_double()
  )
)

p1 <- ggplot(graphs, aes(x=n, y = avgtime)) +
  geom_line(size=1.5) +
  stat_smooth(method="lm", se=TRUE, fill=NA,
                formula=y ~ poly(x, 3, raw=TRUE),colour="red") +
  labs(title="Vpliv števila oglišč na čas", x="Število oglišč", y="Povprečen čas [s]")
print(p1)





