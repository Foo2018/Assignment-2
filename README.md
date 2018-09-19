# Assignment Two - Code Smells
## 1.	Bad Smell One
### Code Smell Name: 
Long Method
### Location:
`extractor.py` > Class name – Extractor() > Method name - `_data_extraction()` > Lines 48 - 84 
### Reasons: 
* Longer than the recommended 10 lines – It has 36 lines
* Code grew in length as more and more search features were added. 
* The code is hard to follow as there are a number of ‘if’ and ‘elif’ statements each of which has a separate purpose
* It will be much easier to read the method code and follow what it is doing with properly named methods, broken down into smaller chunks
* Because the code is complicated to follow due to its length it is going to be the hardest to maintain and the most susceptible to having errors introduced into it. It is a critical part of the extractor feature so should something go wrong the result is fatal for the module. It is therefore the worst of the three smells I have identified.
### Refactoring strategies/ approaches
In order to reduce the size of the method I will be using;
* **Extract methods**: I have identified 5 areas within the  _data_extraction() code that would benefit from being extracted out as methods thus reducing the original method size. These are:
  * Lines 51 - 53. This area provides functionality to search a line of text and extract class, function and attribute names. It then gives feedback as to which has been found
  * Lines 55 - 56. This provides functionality that creates a Component object and names it as the discovered class name
  * Lines 57 - 65. This area provides the ability to search for object parent names and also creates a new stub object where a parent class is not known to the program.
  * Lines 67 - 74. Functionality to place a function name into the correct component object and also error capture if that component object has not been created yet
  * Lines 76 - 84  Functionality to place a attribute name, type and default value into the correct component object and also error capture if that component object has not been created yet 
### Result:
* Five methods were extracted (Lines numbers the method replaced, followed by method name):
  * Lines 51 - 53 - `class_parameter_extractions`
  * Lines 55 - 56 - `_set_class_name()`
  * Lines 57 - 65 - `_class_parent_name_handling()`
  * Lines 67 - 74 - `_place_function_name_in_component_object()`
  * Lines 76 - 84 - `_place_attribute_name_and_default_value_in_dictionary`
* As a result of refactoring the _data_extraction method within the Extractor class I was able to reduce the size of that method from 36 to 11 lines. A considerable reduction and it is now a very easily maintainable method. 
* By extracting chunks of code into their own methods and then giving those methods very descriptive names and renaming existing variables I not only removed explanatory commenting (A bad smell in its own right) but I made the code much more readable. For example:
`elif is_attribute_name: self._place_attribute_name_and_default_value_in_dictionary(is_attribute_name, line)` can be read directly from the code as "if is attribute name place attribute name and default value in dictionary". This is much clearer and easier to understand. Again this aids maintainability and understanding of the code.


## 2.	Bad Smell Two
### Name:
Large Class
### Location:
`extractor.py` > Class name – Extractor() > Lines 17 - 175 
### Reasons: 
* The Extractor class is currently a lengthy class with 11 methods 
* The number of methods will increase once the method extraction for bad smell one is completed
* There are two obvious parts to the current class. Methods that place items in Component objects/ dictionaries and those that search text for relevant class diagram categories
* There is potential for further types of data extraction to be required if more functionality is required in the future, for example extracting accessibility data. This will then increase the number of methods that undertake text search. By placing the two parts into separate classes this avoids one large bloated class and improves the maintainability of the classes.
* This is the second worst smell of the three I have identified. A lengthy class has been created and it is an effort to read and understand in its entirety. Splitting into two classes will improve readability, therefore maintainability.   
### Refactoring strategies/ approaches
* **Extract Class**: This class effectively does the work of two. There are two clear areas of functionality.
1. Collate class properties such as class names, function names and attribute names, values and types into dictionaries and ultimately component objects. This was initially handled by the:
   *  `_data_extraction()` method.

   After refactoring to clear the 'Long Class" smell from the `_data_extraction()` method. the following methods were extracted and added to the Extractor class to also deal with data collation.
    * `class_parameter_extractions()`
    * `_set_class_name()`
    * `_class_parent_name_handling()`
    * `_place_function_name_in_component_object()`
    * `_place_attribute_name_and_default_value_in_dictionary`  
 
2. The second area of functionality for the Extractor class is searching input text for class properties and returning the results. This is handled by:
   * `_regex_search()`
   * `_extract_class()`
   * `_extract_parents()`
   * `_extract_functions()` 
   * `_extract_attributes()`
   * `_extract_defaults_data_types()`
   * `_extract_attribute_defaults()`
   * `_extract_attribute_data_types()`

As can be seen the Extractor class, as well as being large, does not have single-responsibility. There are two clear purposes to the class. In particular the search aspect would likely be enlarged as the program becomes more sophisticated, thus adding to the class size, complexity and chance of breaking the collation side. Extracting a class from the existing Extractor class will increase its robustness. Therefore using the Extract Class refactoring method I will be extracting at least one class from the original based on the text search methods.

### Result
Upon examining the extraction methods that I wished to put into another class I decided that there were actually three different viable classes that could be made, each with a single search focus. These were:
* A class to search specifically for class, function and attribute names. The returned values for these were all the same type (list) and along with their similar functionality it made sense to group them together. The class created was **ClassParameterSearch** 
* A class to search for and extract any parent class name(s) that an object may have. The class created was **ParentExtraction**
* A class to search for and extract attribute defaults and data types. The class created was **AttributeDefaultsSearch**

As can be seen these all have single responsibility and encapsulate methods that work on one type of data.The transition to having three classes over and above to the Extractor class has worked very well and I am very pleased with the extra flexibility and future-proofing that it introduces into the program. 

Creating these classes did, however, have the side effect of creating a new bad smell - "Duplicate Code".   

## 3.	Bad Smell Three
### Name:
Duplicate Code
### Location:
* `class_parameter_search.py` > Class name – ClassParameterSearch() > Method name - `_regex_search()` > Lines 19 - 23 
* `parent_extraction.py` > Class name – ParentExtraction() > Method name - `_regex_search()` > Lines 19 - 22
* `attribute_default_search.py` > Class name – AttributeDefaultsSearch() > Method name - `_regex_search()` > Lines 11 - 15
### Reasons:
* In the original Extractor class there was one instance of `_regex_search()` which served all search functions within that method. 
* Once the Extractor class was devolved into three extra classes the `_regex_search()`method had to be included in each class in order for the encapsulated methods to work.
* After reviewing the code some time after it had been written it was established that although there were now slight variations in the `_regex_search()` method that they were effectively the same code.
* Having a method that either repeats itself exactly or similarly over several classes makes maintainability and robustness an issue. If a change were to be made in how the search was undertaken or what parameters the method takes in then it would require another smell, 'Shotgun Surgery' to fix it. This, therefore, is why this is my third most important smell 
### Refactoring strategies/ approaches
* **Extract Superclass**: In order remove duplication of the regex search code that is common to all three classes it will be necessary to use the Extract Superclass refactoring technique. I will create a super class that will contain the `_regex_search()` method. All three search classes will inherit from this and therefore have access to it. 
### Result
I have created a super class using a Python abstract class. It is called **SearchAbstract**. The super class name and functionality fits nicely with the three sub-classes. It allows for further shared methods to be easily added to the search group of classes if needed in the future.  This class does not have to be instantiated in order to function. I have placed the `_regex_search()` method within this class. As mentioned previously the `_regex_search()` method varied slightly in the ParentExtraction class. I considered that it was appropriate and worthwhile to change the ParentExtraction code to fit a more generic version of the `_regex_search()` method thus allowing use of it in the super class. This refactoring has been very successful and allows for easy expansion of the code and more search classes to be added on whilst maintaining the robustness of the program  

## 4.	Bad Smell Four
### Name:
Switch Statements
### Location:
`attribute_default_search.py` > Class name – AttributeDefaultsSearch() > Method name - `_extract_attribute_data_types()` > Lines 150 -171
### Reasons: 
* The `_extract_attribute_data_types()` method contains a long 'elif' statement. This falls into the 'Switch Statements'smell
* There are no switch statements in Python but long 'elifs' are the equivalent and are considered to not be good OOP practice
* Switch (elifs) can introduce complications and can grow unwieldy over time, becoming hard to be maintained.
* This particular 'elif' does have the potential to grow very large as the program becomes more sophisticated and requires more items to be searched for
### Refactoring strategies/ approaches
The approaches that were experimented with were:
* Replacing conditional with polymorphism
* Replace type code with Strategy
* Replace nested conditional with guard clauses
 
### Result
I considered and tried a number of approaches to reduce this 'elif' statement. I looked at ways to introduce polymorphism but I felt that the search data, being mostly singular, non-alphabetic characters did not lend themselves to my understanding of this method which uses classes. I tried a number of ways but could not get it to work. Using a strategy pattern is another way of dealing with conditionals but I had similar issues to polymorphism. I feel that these two approaches were probably overkill for this particular example. Another 'pythonic' approach was to place the input data in a dictionary as keys and have the return data as values. This worked very well for most situations, however two comparisons in the 'elif' use the Python string methods isalpha() and isdigit() and these would not translate to being used as a dictionary key. I tried a hybrid of using the isalpha() and isdigit() still within an elif statement combined with the remaining comparisons within a dictionary. I was not happy with the results.
Lastly I tried using 'guard clauses'. This worked fine and has simplified the look of the statement overall and introduces a flat structure. This elif clause performs relatively simple actions but does have the potential to become unwieldy so can benefit from some refactoring as I have done.   



