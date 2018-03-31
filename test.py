import net
import stochastic

n = net.Net()
n.generate(5, 10, stochastic.Stochastic())
n.print_characteristics()
