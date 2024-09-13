/*1. List the names, first names and dates of birth of all the students.*/
SELECT NOM, PRENOM, DATE_NAISSANCE FROM ELEVES;

/*2. Provide full information on all activities.*/
SELECT * FROM ACTIVITES;

/*3. Obtain the names of the students whose weight is between 60 and 80 kilos.*/
SELECT NOM FROM ELEVES WHERE POIDS BETWEEN 60 AND 80;

/*4. Obtain the names of professors whose specialty is ”poésie” or SQL.*/
SELECT NOM FROM PROFESSEURS WHERE SPECIALITE IN ('poésie', 'sql');

/*5. Obtain the names of students whose names begin with ”L”.*/
SELECT NOM FROM ELEVES WHERE NOM LIKE 'L%';

/*6. Obtain the names of professors whose specialties are unknown.*/
SELECT NOM FROM PROFESSEURS WHERE SPECIALITE IS NULL;

/*7. Obtain, for each professor, his name and his specialty. If the speciality is unknown, we
want to display the character string: ‘****’.*/
SELECT NOM,
       CASE 
          WHEN SPECIALITE IS NULL THEN '****'
          ELSE SPECIALITE
       END AS SPECIALITE
FROM PROFESSEURS;

/*8. What are the first and last names of the students who practice surfing at level 1. Write
this query in at least three different ways.*/
SELECT E.PRENOM, E.NOM FROM ELEVES E
JOIN ACTIVITES_PRATIQUEES AP ON E.NUM_ELEVE = AP.NUM_ELEVE
WHERE AP.NOM = 'Surf' AND AP.NIVEAU = 1;

SELECT E.PRENOM, E.NOM FROM ELEVES E, ACTIVITES_PRATIQUEES AP
WHERE E.NUM_ELEVE = AP.NUM_ELEVE AND AP.NOM = 'Surf' AND AP.NIVEAU = 1;

SELECT E.PRENOM, E.NOM FROM ELEVES E
WHERE EXISTS (
    SELECT 1
    FROM ACTIVITES_PRATIQUEES AP
    WHERE AP.NUM_ELEVE = E.NUM_ELEVE AND AP.NOM = 'Surf' AND AP.NIVEAU = 1
);

/*9. Obtain peer names of professors who have the same specialty.*/
SELECT P1.NOM AS Professeur1, P2.NOM AS Professeur2, P1.SPECIALITE FROM PROFESSEURS P1
JOIN PROFESSEURS P2 ON P1.SPECIALITE = P2.SPECIALITE AND P1.NUM_PROF < P2.NUM_PROF;

/*10. For each professor, display his hiring date, his date of last promotion as well as the
number of years elapsed between these two dates.*/
SELECT NOM, DATE_ENTREE,DER_PROM,
    EXTRACT(YEAR FROM DER_PROM) - EXTRACT(YEAR FROM DATE_ENTREE) AS ANNEES
FROM PROFESSEURS;

/*11. Display the average age of students. This average age will be expressed in years.*/
SELECT FLOOR(AVG(MONTHS_BETWEEN(SYSDATE, DATE_NAISSANCE) / 12)) AS AVG_AGE
FROM ELEVES;

/*12. Obtain the list of students who will be at least 24 years old in less than 4 months.*/
SELECT NOM FROM ELEVES
WHERE ADD_MONTHS(DATE_NAISSANCE, 288) < ADD_MONTHS(SYSDATE,4);

/*13. Obtain the name and the average for each 1st year student.*/
SELECT E.NOM, AVG(R.POINTS) AS MOYENNE FROM ELEVES E
JOIN RESULTATS R ON E.NUM_ELEVE = R.NUM_ELEVE
WHERE E.ANNEE = 1
GROUP BY E.NOM;

/*14. Which 1st year students have an average higher than the 1st year average?*/
SELECT E.NOM, E.PRENOM, AVG(R.POINTS) AS moyenne_eleve FROM RESULTATS R
JOIN ELEVES E ON R.NUM_ELEVE = E.NUM_ELEVE WHERE E.ANNEE = 1
GROUP BY E.NOM, E.PRENOM
HAVING AVG(R.POINTS) > (
    SELECT AVG(R2.POINTS) FROM RESULTATS R2
    JOIN ELEVES E2 ON R2.NUM_ELEVE = E2.NUM_ELEVE WHERE E2.ANNEE = 1
);

/*15. Obtain the name and weight of grade 1 students heavier than any grade 2 student.*/
SELECT NOM, POIDS FROM ELEVES
WHERE ANNEE = 1 AND POIDS > ALL (SELECT POIDS FROM ELEVES WHERE ANNEE = 2);

/*16. Obtain the name, weight and grade of students weighing more than the average weight
of students in the same grade.*/
SELECT NOM, POIDS, ANNEE
FROM ELEVES E1
WHERE POIDS > (SELECT AVG(POIDS)
               FROM ELEVES E2
               WHERE E1.ANNEE = E2.ANNEE);

SELECT ANNEE, AVG(POIDS) AS AVG_POIDS FROM ELEVES GROUP BY ANNEE; /* Moyenne des poids pour chaque année pour vérifier*/

/*17. Obtain the names of teachers who are not teaching class 1.*/
SELECT DISTINCT p.NOM FROM PROFESSEURS p
WHERE p.NUM_PROF NOT IN (SELECT c.NUM_PROF FROM CHARGE c WHERE c.NUM_COURS = 1);

/*18. Obtain the names of grade 1 students who have obtained more than 60% points and
who play tennis.*/
SELECT e.NOM FROM ELEVES e JOIN RESULTATS r ON e.NUM_ELEVE = r.NUM_ELEVE
JOIN ACTIVITES_PRATIQUEES ap ON e.NUM_ELEVE = ap.NUM_ELEVE
WHERE e.ANNEE = 1 AND ap.NOM = 'Tennis'
GROUP BY e.NUM_ELEVE, e.NOM
HAVING AVG(r.POINTS) > 12;

SELECT e.NUM_ELEVE, e.NOM AS ELEVE, /* Vérifications */
       AVG(r.POINTS) AS AVG_POINTS
FROM ELEVES e
JOIN RESULTATS r ON e.NUM_ELEVE = r.NUM_ELEVE
WHERE e.ANNEE = 1
GROUP BY e.NUM_ELEVE, e.NOM;


/*19. Teachers who take charge of all the second year courses; we ask for the Number and the
name.*/

/*20. Students who practice all the activities; we ask for the Number and the name.*/
