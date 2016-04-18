# -*- coding: utf-8 -*-
from __future__ import division
import codecs
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import beta
from scipy.misc import comb
from scipy.interpolate import interp1d

sim  = sorted([ l.strip().split()[-2] for l in codecs.open('sim.txt',       'rt', 'utf-8').readlines() ])
nao  = sorted([ l.strip().split()[-2] for l in codecs.open('nao.txt',       'rt', 'utf-8').readlines() ])
abst = sorted([ l.strip().split()[-2] for l in codecs.open('abst.txt',      'rt', 'utf-8').readlines() ])
falt = sorted([ l.strip().split()[-2] for l in codecs.open('faltantes.txt', 'rt', 'utf-8').readlines() ])

# Assume um prior Beta (para facilitar a vita) com a moda igual à proporção 
# observada e precisão proporcional ao tamanho da observação. A fórmula dos 
# parâmetros alfa e beta em função da moda vieram daqui :
# http://doingbayesiandataanalysis.blogspot.com.br/2012/06/beta-distribution-parameterized-by-mode.html
nObs      = len(sim)+len(nao)+len(abst)
priorModa = len(sim)/nObs
priorA    = priorModa*(nObs-2)+1
priorB    = (1-priorModa)*(nObs-2)+1

print 'sim=', len(sim), 'nao=', len(nao), 'abst=', len(abst), 'prior sim=', priorModa

todos    = sorted(sim+nao+abst+falt)
votos    = sorted(sim+nao+abst)
partidos = set(todos)

# Calcula os posteriors para cada partido, com a regra de Bayes
simRange = np.linspace(0.0, 1.0, 101, endpoint=True)
suportes = []
probabs  = [] 
for p in partidos :
	# Queremos estimar, fração_sim_p, a fração dos representantes no partido p
	# que ainda irão votar sim, dada as observações dos membros desse partido 
	# que já votaram.

	# Pr(fração_sim_p|obs) = Pr(fração_sim_p) * Pr(obs|fração_sim_p) / p(obs)
	# Pr(fração_sim_p) é o prior Beta
	# a verossimilhança Pr(obs|fração_sim_p) é uma Binomial 
	#	com n=len(votos), p=fração_sim_p, e k=sim.count(p) 
	# verossim  = binom.pmf(sim.count(p), len(votos), simRange)

	# Devido à Beta ser conjugada da Binomial, o posterior Pr(fração_sim_p|obs) 
	# pode ser calculado analiticamente (por fórmula) e é uma BetaBinomial
	def BetaBinomial(n, k, A, B) :
		# for n trials, k successes, alpha=A, beta=B
		return comb(n, k) * beta(A+k, B+n-k) / beta(A, B)

	if falt.count(p) > 0 :
		# distribs.append([ suporte, probability ])
		n = votos.count(p)
		suporte   = np.arange(0, n+1, 1)
		posterior = np.array([ BetaBinomial(n, k, priorA, priorB) for k in suporte ])
		# print 'Suporte.size = ', suporte.size
		if suporte.size == 1 :
			suporte   = np.concatenate( [ suporte-1 , suporte, suporte+1 ] )
			posterior = np.concatenate( [ [ 0.0 ], posterior, [ 0.0 ] ] )
		suportes.append(suporte)
		probabs.append(posterior)
	else :
		suportes.append(np.array([ -1.0, 0.0, 1.0  ]))
		probabs.append(np.array([ 0.0, 1.0, 0.0 ]))

print 'Interpolando...'
suporte = np.concatenate(suportes)
suporte = np.unique(suporte)
print suporte
suporte = np.arange(suporte[0], suporte[-1]+1, 1)
print '***************************'
print suporte
interps = []
for distrib in zip(suportes, probabs) :
	# print distrib[0]
	interp = interp1d(distrib[0], distrib[1], 'linear', bounds_error=False, fill_value=0.0)
	interp = interp(suporte)
	print 'Distrib:', np.sum(distrib[1]), 'Interp:', np.sum(interp)
	interps.append(interp)


distribFinal = np.array([ 1.0 ])
print 'Convoluindo...'
for interp in interps :
	print 'Passo, ', interp.shape, distribFinal.shape, np.sum(distribFinal)
	distribFinal = np.convolve(distribFinal, interp, 'full')

print distribFinal.shape, np.sum(distribFinal), distribFinal

# meio   = distribFinal.size // 2
# inicio = meio - (suporte.size // 2)
# distribFinal = distribFinal[inicio:inicio+suporte.size]

novosuporte=np.arange(0, distribFinal.size, 1)
fig, ax = plt.subplots(1, 1)
ax.plot(novosuporte, distribFinal)
#ax.legend(loc='sim adicionais aos '+str(len(sin)), frameon=False)
plt.show()
