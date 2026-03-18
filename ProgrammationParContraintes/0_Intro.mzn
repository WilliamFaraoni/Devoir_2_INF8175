% NOM_ETUDIANT_1 (MATRICULE_1)
% NOM_ETUDIANT_2 (MATRICULE_2)

include "globals.mzn";

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Nombre devant satisfaire les critères
var 1000..9999: nombre;

% Décomposition du nombre en un ensemble de chiffres
array[1..4] of var 1..9: chiffres;

%-----------------------------------------------------------------------------%
% Objectif
%-----------------------------------------------------------------------------%

% Variable à minimiser
var int: p;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%
%constraint nombre mod 2 = 0;
%constraint nombre > 1000;%chiffres[1] > 0 /\ chiffres[2] > 0 /\ chiffres[3] > 0 /\ chiffres[4] > 0;

constraint nombre = chiffres[1]*1000 + chiffres[2]*100 + chiffres[3]*10 + chiffres[4];
constraint chiffres[4] mod 2 = 0;%C’est un nombre pair.
constraint chiffres[1] > 0 /\ chiffres[2] > 0 /\ chiffres[3] > 0 /\ chiffres[4] > 0;%Le chiffre 0 n’est pas présent dans le nombre.
constraint chiffres[1] != chiffres[2] /\ chiffres[1] != chiffres[3] /\ chiffres[1] != chiffres[4]
           /\ chiffres[2] != chiffres[3] /\ chiffres[2] != chiffres[4]
           /\ chiffres[3] != chiffres[4];%Les 4 chiffres sont différents.
constraint chiffres[1] > chiffres[2];%Le chiffre à la position des milliers est supérieur à celui à la position des centaines.
constraint chiffres[3] < chiffres[4];%Le chiffre à la position des dizaines est inférieur à celui à la position des unités.
constraint chiffres[2] > chiffres[4];%Le chiffre à la position des centaines est supérieur à celui à la position des unités.
constraint 15 < chiffres[1] + chiffres[2] + chiffres[3] + chiffres[4];%La somme des 4 chiffres est supérieure à 15.
constraint p = chiffres[2] * chiffres[3] * chiffres[4];%Le produit des 3 derniers chiffres (chiffre à la position des centaines×chiffre à la position des dizaines × chiffre à la position des unités) doit être minimisé.

solve minimize p;%Le produit des 3 derniers chiffres (chiffre à la position des centaines×chiffre à la position des dizaines × chiffre à la position des unités) doit être minimisé.

%solve satisfy;
%-----------------------------------------------------------------------------%

output [
  show(nombre)
];

