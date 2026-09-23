# Commands used with agent
## Github-Copilot

As the free version is being used, it automatically decides which model to use

---
## Hash checker
- Went well, which includes expected issue in assuming that the hash can match any or even all types of algorithm (if algorithms are different, the hash will be different between them)
- 6.5/10, the .5 is due to the (expected) incorrectly assumed behaviour

### 1st command
```
Generate python script that receives a file, 
calculates the checksum with MD5, SHA-256 and SHA-1, 
and compares to a given hash that notifies if a match is found or not
```

### Additional requests:
```
Generate and document tests for possible cases of script
``` 
(+Script reference/context)

```
Generate documentation for script
``` 
(+Script reference/context)

---

## Setup folder structure for an agent or a project
- Maybe, given the previous request specified a python script, it assumed the new script(s) should also be in python
- Despite in a command only "Review and verify" were stated, it assumed it should apply changes to discovered issues (not an issue in this case, but to be noted)
- Only does the bare minimum of all bare minimums, i.e., requires specifying everything, as it originally was only generating a (single) new folder with only a .md file plus a file for the given language

### 1st request - Agent
```
Create a script that generates a template agent file structure
Explain the methodology and choices
```

### 1st request - Project
- Interesting in that it added the result of the request "Explain process and choice making" to the .md files despite the .md rewrite request being in different lines
```
Explain process and choice making
In folder "Scaffolding"
Create a separate script that scaffolds a project folder and generates boilerplate code for apps in C# or Java
Rewrite the .md files plus add description and explanation for scripts with tests
```

### Additional Requests
In previous command, forgot to specify or ask it to verify the latest C# or Java versions to use, so the script initially used .NET 8 and java 17
```
Explain why choose for C# .NET 8 and for Java 17
```

```
Verify what are the latest lts versions for C# and Java
```

```
Choose only one, either generate a new scaffold project script for the latest versions or edit the existing one to use different possible versions
Explain the choice made
```

- Attempt to guarantee that the program/script could run on any/most machines
```
Review and verify that all generated scripts are independent of platform and operating system
```

- As I lack experience with python, I asked it to generate a new version in C++, so as to better understand, analyse and verify the results
- It correctly assumed this time that the C++ program should have the behaviour of both (agent and project) scripts
```
Verify what is the latest stable version of C and C++
Create a new folder and recreate the scaffolding scripts into a C++ program
Add ability to also generate in C or C++
Make it independent of platform and Operating System
Add documentation
```

- After noticing that the agent only does the bare minimum of all bare minimums
```
Edit and update script to generate different possible project file structures, such as
common production project,
website with frontend, backend and database
```

- Command not fully written was accidentally sent, but interesting result in the agent assuming that the "Add template graphical interface code" was meant for the script itself and not as a new possible generation option
```
Separate content and text of templates from the code itself to improve scalability and readability
Add template graphical interface code
```

- Didn't do anything
```
Create a repository in github using the AI folder
```

#### Additional behaviour plus update to C++ version
```
Add support for a MVC project structure
Update native_scaffold.cpp to reflect all changes made to script
```

- It had not fully updated the C++ version, so an additional command was needed
```
Separate content and text of templates from the code itself to improve scalability and readability
Rewrite, reorganize and clean the resulting code
```

It suggested
> (...)
> If you want, I can next tighten the native template catalog further by adding shared template metadata or a small README for the template folder itself.

- Additionally it did not have a makefile, assuming that is due to the program being a single file and it not being specified
```
Do that
Create a make file for the NativeScaffolding, use wsl to test if needed
```

- Performed with acceptable results 
```
Review and verify if issues remain
Suggest code optimization
```
```
Perform optimization suggestions
```