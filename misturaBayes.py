from __future__ import division
import codecs
sim  = sorted([ l.strip().split()[-2] for l in codecs.open('sim.txt',       'rt', 'utf-8').readlines() ])
nao  = sorted([ l.strip().split()[-2] for l in codecs.open('nao.txt',       'rt', 'utf-8').readlines() ])
abst = sorted([ l.strip().split()[-2] for l in codecs.open('abst.txt',      'rt', 'utf-8').readlines() ])
falt = sorted([ l.strip().split()[-2] for l in codecs.open('faltantes.txt', 'rt', 'utf-8').readlines() ])
# assume ingenuamente um prior equivalente a proporcao do total
prior = len(sim)/(len(sim)+len(nao)+len(abst))
print 'sim=', len(sim), 'nao=', len(nao), 'abst=', len(abst), 'prior sim=', prior
todos = sorted(sim+nao+abst+falt)
partidos = set(todos)
totalSim = 0.0
for p in partidos :
	# p(sim | partido) = p(sim) * p(partido | sim) / p(partido)
	probPartidoDadoSim = sim.count(p)/len(sim)
	probPartido = todos.count(p)/len(todos)
	posterior = prior * probPartidoDadoSim/probPartido
	pFalt = falt.count(p)
	mistura = pFalt*posterior
	print p, ':\t', pFalt, '*', posterior, '=', mistura
	totalSim += mistura
print 'falt=', len(falt), 'falt sim=', totalSim
