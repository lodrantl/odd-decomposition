library(tidyverse)

small_graphs = read_csv(
  "small_graphs.csv",
  col_types = cols(
    .default = col_integer(),
    percentage = col_double(),
    time = col_double()
  )
)

p1 <- ggplot(small_graphs, aes(x=n)) +
  geom_line(aes(y = percentage)) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 1)) +
  labs(title="Uspešnost razbitja na dva liha podgrafa", x="Število oglišč", y="Uspešnost")
print(p1)

p2 <- ggplot(small_graphs, aes(x=n)) +
  geom_line(aes(y = all, colour="vsi primeri")) +
  geom_line(aes(y = decomposable, colour="uspešni primeri razbiti")) +
  geom_line(aes(y = time*8000, colour="čas izvajanja")) +
  scale_y_continuous("Število primerov", sec.axis = sec_axis(~ . / 8000, name = "Čas v [s]")) +
  labs(title="Število primerov", x="Število oglišč") +
  theme(legend.title = element_blank())
print(p2)





