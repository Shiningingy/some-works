%Allen Luo
%20001744

pairFlip([],[]).
pairFlip([X],[X]).
pairFlip([X1,X2|XS],[X2,X1|YS]) :- pairFlip(XS,YS).



sublist([],_).
sublist([X|XS],[X|XSS]):-sublist(XS,XSS).
sublist([X|XS],[_|XSS]):-sublist([X|XS],XSS).



listSum([],0).
listSum([X1|XS],Total):-
    listSum(XS,SubSum),
    Total is X1+SubSum.



sublistSum(L1,SUM,L2):-
    sublist(L2,L1),
    listSum(L2,SUM).


listSumStr([X1,X2,X3],X1+X2+X3).


courseStudent([],[]).
courseStudent([X|XS],[[S1,S2]|SS]):-
    listSumStr([S1,S2,_],X),
    courseStudent(XS,SS).


legalCourse([]).
legalCourse([X|XS]):-
    listSumStr([Student1,Student2,_],X),
    Student1 \= Student2,
    courseStudent(XS,StudentList),
    \+ sublist([[Student1,Student2]],StudentList),
    \+ sublist([[Student2,Student1]],StudentList),
    legalCourse(XS).



nameInCourse(Name,[Name,_],1).
nameInCourse(Name,[_,Name],1).
nameInCourse(Name,[S1,S2],0):-
    Name \= S1,
    Name \= S2.

studentCount(_,[],0).
studentCount(Name,[Acourse|Courses],Count):-
    listSumStr([Student1,Student2,_],Acourse),
    nameInCourse(Name,[Student1,Student2],InCourse),
    studentCount(Name,Courses,SubCount),
    Count is SubCount + InCourse.



partner(Name,[Name,Partner],Partner).
partner(Name,[Partner,Name],Partner).

partners(_,[],[]).
partners(Name,[Acourse|Courses],[Partner|PS]):-
    listSumStr([Student1,Student2,_],Acourse),
    partner(Name,[Student1,Student2],Partner),
    partners(Name,Courses,PS).

partners(Name,[Acourse|Courses],List):-
   listSumStr([Student1,Student2,_],Acourse),
   nameInCourse(Name,[Student1,Student2],0),
   partners(Name,Courses,List).

courseSum([],0).
courseSum([Acourse|Courses],Total):-
    listSumStr([_,_,CourseMark],Acourse),
    courseSum(Courses,SubTotal),
    Total is CourseMark + SubTotal.

courseAvg(CourseList,Avg):-
   courseSum(CourseList,Total),
   length(CourseList,Len),
   Avg is Total/Len.


studentSum(_,[],0).

studentSum(Name,[Acourse|Courses],Total):-
    listSumStr([Student1,Student2,_],Acourse),
    nameInCourse(Name,[Student1,Student2],0),
    studentSum(Name,Courses,SubTotal),
    Total is 0+ SubTotal.


studentSum(Name,[Acourse|Courses],Total):-
    listSumStr([Student1,Student2,CourseMark],Acourse),
    nameInCourse(Name,[Student1,Student2],1),
    studentSum(Name,Courses,SubTotal),
    Total is CourseMark + SubTotal.



studentAvg(Name,CourseList,Avg):-
    studentSum(Name,CourseList,Total),
    studentCount(Name,CourseList,Count),
    Avg is Total/Count.


studentInList(Name,[Name|_]).
studentInList(Name,[_|Students]):- studentInList(Name,Students).

studentsList([],[]).
studentsList([Acourse|Courses],[Student1,Student2|SubList]):-
    listSumStr([Student1,Student2,_],Acourse),
    studentsList(Courses,SubList).


removeDupeNames([],Alist,Alist).
removeDupeNames([Student|Students],Alist,Result):-
    member(Student,Students),
    removeDupeNames(Students,Alist,Result).

removeDupeNames([Student|Students],Alist,Result):-
    not(member(Student,Students)),
    removeDupeNames(Students,[Student|Alist],Result).


students(CourseList,Result):-
    studentsList(CourseList,StudentList),

%   removeDupeNames(StudentList,[],Result).
%
%   Method Above is also work but produce different order from the
%   sample.
%
    sort(StudentList,Result).


