TITLE Calcium dynamics for RD Traub, J Neurophysiol 89:909-921, 2003

COMMENT

	Implemented by Maciej Lazarewicz 2003 (mlazarew@seas.upenn.edu)

ENDCOMMENT

NEURON {
	SUFFIX cad_cc
	USEION ca READ ica WRITE cai
	RANGE phi, beta
	GLOBAL ceiling
}

UNITS {
	(mA)	= (milliamp)
	(mM) = (milli/liter)
}

PARAMETER {
	phi		(100/coulomb meter)
	beta		(/ms)
	ceiling		(mM)
}

STATE {	cai (mM) }

INITIAL { 
	cai = 0 : 50e-6 
}

ASSIGNED { 
	ica		(mA/cm2) 
}
	
BREAKPOINT {
	SOLVE state METHOD cnexp
	if( cai < 0 ){ cai = 0 }
	if( cai > ceiling ){ cai = ceiling }
}

DERIVATIVE state { 
:	cai' = - phi * ica - beta * (cai - 50e-6) 
	cai' = - phi * ica - beta * (cai) 
}
