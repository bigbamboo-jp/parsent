# parsent
A Python module for analyzing parts of a sentence enclosed by specific symbols.

## Features
* Separation of parts enclosed by specific symbols from those that are not.
* Hierarchical classification of parts enclosed by specific symbols within another enclosed part.
* Ability to set multiple types of delimiters in a single process.
* Grouping of only specific parts when classification of lower hierarchies is not needed.

## How to use
1. Importing the parsent module  
Note: To import as shown below, the program from which you're importing and the parsent module must be in the same directory.
    ```
    import parsent
    ```
2. Sentence Analysis  
Analyze the sentence and obtain a SentenceStructureInformation object.
    ```
    result = parsent.analyze_sentence('This is a "test".', ('"', '"'))
    ```
    Note: Although not specified here, the `delimiter_handling_mode` argument can be provided to the `analyze_sentence` function. By specifying this, delimiters can be attached to the part itself or not attached anywhere.  
    Also, by specifying the `consider_escaping` argument, consideration of escaping can be set.  
    To retrieve the original sentence from the SentenceStructureInformation object, do as follows:
    ```
    text = str(result)
    ```
3. Result Verification  
    ```
    print(result.get())
    ```
    Note: To display omitting empty strings, do as follows:
    ```
    print(result.get(omit_empty_strings=True))
    ```
4. Shrinking Analysis Results (optional)  
    In the code below, the hierarchies below the first layer are being declassified.
    ```
    text1 = 'The book says, "[Man] is only one of many creatures on Earth."'
    result1 = parsent.analyze_sentence(text, [('"', '"'), ('[', ']')])
    print(result1.get())
    result2 = result1.shrink_analysis_results(bottom_hierarchy=1)
    print(result2.get())
    ```
5. Utilizing the Analyzed Results  
While the analyzed results can be used for various purposes, here's an example code that displays only the quoted strings.
    ```
    for part in result.get():
        if part[1] == 1:
            print(part[0])
    ```

## Handy Utility Functions
Typically, the data structure obtained from the `get` method of the SentenceStructureInformation object looks like `[['This is a "', 0], ['test', 1], ['".', 0]]`, which is a structure like `[[(string), (hierarchy number)], [(string), (hierarchy number)], ... ]`. There are times when you want to use this in a different format or only want to use some of the information. For such cases, this library is equipped with functions to manipulate the data. Please check the source code to see what functions are available and how they can be used.

## About the Project Name
The name "parsent" is a portmanteau created by combining the functionality of the program, "parse sentences", with "%".

## Licence
Please refer to the [license file](LICENSE).
