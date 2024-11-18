## Gedetailleerde omschrijving
_hier komt een gedetailleerde omschrijving van de issue_

## Aanpassingen aan het domeinmodel
_noteer hier mogelijkse aanpassingen aan het domeinmodel_

## Relevante wireframes
(Link naar de wireframes)

## mogelijkse Api's 
_noteer hier mogelijkse endpoints die nodig zullen zijn voor deze issue_ 

## Acceptatiecriteria
```
  Background:
    Given Students
    | name | email      |  id|
    | Jan  | jan@kdg.be |  1 |
    | Piet | piet@kdg.be|  2 |

    Given Courses
    | name          | id  | credits |
    | Programmeren  | 1   | 6       |
    | Databanken    | 2   | 3       |


    Given CourseSubscriptions
    | studentId | courseId | creditReceived   |
    | 1         | 1        | TRUE             |
    | 1         | 2        | FALSE            |

    Given subscription
    | studentId | year | id |
    | 1         | 2023 | 1  |

    Scenario: Student subscribes to a course
      Given student with id 1 edits subscription with id 1
      When student adds course with id 2
      Then subscription with id 1 has a courseSubscriptions with courseId 2

    Scenario: Student subscribes to a course he already has
        Given student with id 1 edits subscription with id 1
        When student adds course with id 1
        Then subscription with id 1 has a courseSubscriptions with courseId 1
```

## Definition of ready checklist
\[Vink aan welk detail is toegevoegd. Als je eerlijk alles hebt afgevinkt mag je de user story als "refined" beschouwen\]

- [ ] Genoeg detail toegevoegd, de toegewezen ontwikkelaar heeft voldoende detail om de user story zonder bijkomende vragen uit te werken.
- [ ] 1 positief en 1 negatief scenario
- [ ] Nuttige wireframes gekoppeld
- [ ] Gelinkte en blokkerende user stories geïdentificeerd (Linked Items)
- [x] Epic vastgelegd 
- [x] Gewicht vastgelegd
- [x] Prioriteit vastgelegd