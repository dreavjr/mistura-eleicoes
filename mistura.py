from __future__ import division
import codecs
sim  = sorted([ l.strip().split()[-2] for l in codecs.open('sim.txt',       'rt', 'utf-8').readlines() ])
nao  = sorted([ l.strip().split()[-2] for l in codecs.open('sim.txt',       'rt', 'utf-8').readlines() ])
abst = sorted([ l.strip().split()[-2] for l in codecs.open('abst.txt',      'rt', 'utf-8').readlines() ])
falt = sorted([ l.strip().split()[-2] for l in codecs.open('faltantes.txt', 'rt', 'utf-8').readlines() ])
# assume ingenuamente um prior equivalente a proporcao do total
prior = len(sim)/(len(sim)+len(nao)+len(abst))
partidos = set(sim+nao+abst+falt)
totalSim = 0.0
for p in partidos :
	pSim  = len([l for l in sim  if l == p])
	pNao  = len([l for l in nao  if l == p])
	pAbst = len([l for l in abst if l == p])
	pFalt = len([l for l in falt if l == p])
	if (pSim+pNao+pAbst == 0) :
		mistura = pFalt*prior 
	else :
		mistura = pFalt*(pSim/(pSim+pNao+pAbst))
	print p, mistura
	totalSim += mistura
print totalSim
