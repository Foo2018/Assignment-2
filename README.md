"# Assignment2" 
Assignment Two - Code Smells
1.	Bad Smell One
Code Smell Name: Long Method
Location: umlify2 > Extractor.py > Class name – Extractor() > Method name - _data_extraction() > Lines 48 - 84 
Reasons: 
•	Longer than the recommended 10 lines – It has 36 lines
•	Code grew in length as more and more search features were added. 
•	The code is hard to follow as there are a number of ‘if’ and ‘elif’ statements each of which has a separate purpose
•	It will be much easier to read the method code and follow what it is doing with properly named methods, broken down into smaller chunks
•	Because the code is complicated to follow due to its length it is going to be the hardest to maintain and the most susceptible to having errors introduced into it. It is a critical part of the extractor feature so should something go wrong the result is fatal for module. It is therefore the worst of the three smells I have identified.
Refactoring strategies/ approaches
In order to reduce the size of the method I will be using;
•	Extract methods:
•	Decompose conditional:
•	Replace Method with Method Object:
Result:
•	As a result of refactoring the _data_extraction method within the Extractor class I was able to reduce the size of that method from 36 to 11 lines. A considerable reduction

2.	Bad Smell Two
Name: Large Class
Location: umlify2 > Extractor.py > Class name – Extractor() > Lines 17 - 175 
Reasons: 
•	The Extractor class is currently a lengthy class with 11 methods 
•	The number of methods will increase once the method extraction for bad smell one is completed
•	There are two obvious parts to the current class. Methods that place items in Component objects/ dictionaries and those that search text for relevant class diagram categories
•	There is potential for further types of data extraction to be required if more functionality is required in the future, for example extracting accessibility data. This will then increase the number of methods that undertake text search. By placing the two parts into separate classes this avoids one large bloated class and improves the maintainability of the classes.
•	This is the second worst smell of the three I have identified. A lengthy class has been created and is an effort to read and understand in its entirety. Splitting into two classes will improve readability, therefore maintainability.   
Refactoring strategies/ approaches
Result

3.	Bad Smell Three
Name: Switch Statements
Location: umlify2 > Extractor.py > Class name – Extractor() > Method name - _data_extraction() > Lines 48 - 84 
Reasons: 

Refactoring strategies/ approaches
Result


4.	Bad Smell Four –

Name: Duplicate Code

