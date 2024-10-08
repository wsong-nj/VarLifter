# VarLifter, a tool for recovering variables and types from bytecode of Solidity smart contracts

# Contents

- [Introduction](#introduction)
- [Hardware Dependencies](#hardware-dependencies)
- [Getting Started Guide](#getting-started-guide)
- [Step-by-Step Instructions](#step-by-step-instructions)
	- [Preliminaries](#preliminaries)
	- [Verification](#verification)
- [Reusability Guide](#reusability-guide)
	- [VarLifter in the Package](#varlifter-in-the-package)
	- [Other functionalities](#other-functionalities)
	- [Limitations to the Artifact's Reusability](#limitations-to-the-artifact's-reusability)
	- [Troubleshooting](#troubleshooting)

# Introduction

The artifact presented here is VarLifter, a tool designed to lift state variables and their types from compiled Solidity smart contract runtime bytecode.  VarLifter supports both command-line interface (CLI) and graphical user interface (GUI) for ease of use.

VarLifter supports the claims made in our accompanying paper by providing a means to analyze and recover variables and their types from Solidity runtime bytecode, which enhances the understanding of compiled smart contracts and the analysis of smart contract security. Specifically, our paper claims:

- A static analysis approach and open-source tool, VarLifter, to recover variables (excluding variable names) and their types from low-level Solidity runtime bytecode (no need to execute the contract).
- The effectiveness, efficiency, and advantage of VarLifter: 
  1. Overall, 97.48% precision and 91.84% recall; 
  2. Applicable to different compiler versions and contract sizes;
  3. Efficient analysis, with around 70% contracts being analyzed within 10 seconds for each;
  4. Significantly outperforms the state-of-the-art decompilers in terms of type recovery.

The artifact supports all the aforementioned claims. For the first claim (the main statement of our paper), you can experience the amazing process of VarLifter recovering high-level variable type information from obscure low-level bytecode in the [Getting Started Guide](#getting-started-guide) section (something that previously relied heavily on experts with deep specialized knowledge). For the last claim (the experimental section of the paper), you can verify the relevant results by accessing the statistics in the [Step-by-Step Instructions](#step-by-step-instructions) section (we provide datasets and scripts needed to access the data).

# Hardware Dependencies
To evaluate the VarLifter artifact, the following hardware is required:
- A computer with at least 4 GB of RAM and a modern multi-core processor.

- Approximately 500 MB of free disk space.

- The artifact can run on any major operating system (Windows, macOS, Linux) with Python 3.10 or higher installed.

  However, we strongly recommend using the Linux system. The environment in which we run VarLifter is as follows: A virtual machine with a memory capacity of 32GB and an 8-core CPU (11th Gen Intel® Core™ i7-11700 @ 2.50GHz × 8). The operating system used is Ubuntu 22.04.2 LTS.

# Getting Started Guide

**Prerequisites**: Ensure Python 3.10 or higher is installed on your system.

**Download and Installation**:

- Clone the VarLifter repository from Zenodo：[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12671461.svg)](https://doi.org/10.5281/zenodo.12671461)
- Navigate to the project directory: `cd VarLifter`
- Install the required dependencies: `pip install -r requirements.txt`

**GUI Usage** (recommend):

- To launch the VarLifter GUI: `python3 gui.py`

- Using the GUI:

  - *Enter Bytecode*: Click this button to enter a single runtime bytecode of the Solidity smart contract in the provided entry field.

  - *Run Analysis*: Click this button to analyze the bytecode. The analysis results will be displayed in the output area.

  - *Input Folder Path*: Enter a folder path. This folder should contain several runtime bytecode files (.txt format is OK). This will allow you to use VarLifter to batch process multiple inputs without manually repeating inputs multiple times.

  - *Run Batch Analysis*: This button allows you to analyze multiple bytecode files stored in the selected folder. All analysis results will be displayed in the output area. Each result is separated by "===" and labeled by its corresponding input file name.

  - *Stop Analysis*: Click this button to halt an ongoing analysis process.

- Quick test: We have prepared some test cases in the test suite `../VarLifter/test case` , which you can use directly in GUI. 

  <img src="C:\Users\56299\Desktop\GUI.png" style="zoom:50%;" />

Here，you've done!

**CLI Usage** :

To analyze a single Solidity smart contract bytecode from the command line: `python3 main.py "input"`. Replace `"input"` with your actual runtime bytecode.

# Step-by-Step Instructions

Our evaluation benchmark (see **benchmark.address**) contains 34,832 contracts (contract data can be accessed on https://etherscan.io/ based on the contract addresses in the file). The script `run.py` is responsible for automating the analysis of these contracts (including compilation and type recovery) and saving the results locally. It took us more than 22 days (running 24/7) to analyze all the contracts. If you do not have that much time, we provide a smaller test set (see **test case**) that contains 15 contracts randomly downloaded from Ethereum. VarLifter takes about 10 minutes to analyze them, which ensures you can evaluate our artifact within 30 minutes.

## Preliminaries

1. **Contract File and Contract**: Generally, a contract file (our test cases include 15 contract files) consists of multiple contracts (opening any contract file, you will see several contracts beginning with "contract XXX"). These contracts typically have inheritance relationships, for example, *contract A* inherits *contract B*, and *contract B* inherits *contract C*. In such cases, the child *contract A* can access variables from the parent *contract B* and the grandparent *contract C*. Therefore, the analysis result of *contract A* will include variables from its parent contracts. For the contract files in our test cases, we default to analyzing the bottom-most contracts in the inheritance chain (this will recover as many variables from the contract file as possible).

2. **Output Description**: VarLifter's output is formatted as `<0x*********>uint256 //slot(0x1)`,(`uint256`'s alias is `uint`). In this output, `<0x********>` is the function signature, and `uint256 //slot(0x1)` indicates that the variable located at slot 0x1 has been recovered with the type `uint256`. This format arises because all variables are accessed within functions, so VarLifter analyzes the behavior of each function to recover the variables and their types. Additionally, variable names are not within VarLifter's analysis scope, so in our output, `slot(0x*)` represents the variable located at that position.

   You might see '`missing slot (0x*)`' in our output, indicating that VarLifter identified a variable at `slot (0x*)` but could not determine its type (possibly because the variable was not used). Additionally, you might see ‘`(u)int256/bytes32`’, which represents a set of types: `int256`, `uint256`, and `bytes32`. These types are indistinguishable in the EVM, so when you see ‘`(u)int256/bytes32`’, it could represent any one of these types. This type of output is considered correct.

   You might also see `<0x********> address //slot(0x1) and <0x########> bool //slot(0x1)`. They have the same storage slot, but this does not mean VarLifter erroneously infer a single variable as having two conflicting types. This is due to the EVM's packing mechanism (designed to save gas): as long as the remaining length of a slot (32 bytes) is greater than the length of the next variable, the EVM will store multiple variables in the same slot. In this example, an address type variable occupies 20 bytes, leaving 32 - 20 = 12 bytes in the slot. Since 12 bytes is greater than the length of a bool type variable (1 byte), this variable is also stored in the same slot. So this output indicates that VarLifter recovered two variables from slot (0x1): one of bool type and one of address type, with their combined length being less than one machine word. In contrast, `<0x********> mapping(uint=>address) //slot(0x1) and <0x########> mapping(uint=>address) //slot(0x1)` indicate that VarLifter recovered this variable in different functions (no type conflict, packing condition not met), because different functions might access the same variable.

3. **Correspondence between Output and Ground Truth**: The declaration order of variables in the source code determines their storage location in the storage. For example, if a contract declares variables `address A` and `uint256 B` sequentially, then variable *A* will be stored in the first `slot (0x0)` in the storage, and variable *B* will be stored in the second `slot (0x1)`. Based on this, VarLifter's output can be mapped to the variables in the source code. This correspondence is crucial to verify whether the recovered types are correct. For example, for the output "`uint256 //slot(0x1)`", it indicates the second declared variable in the source code, and its type is `uint256`, which corresponds to variable B, and we can determine that this result is correct. 

## Verification

Once you have executed all the input test cases in the test case `../VarLifter/test case` (using the batch run button in the GUI, which takes approximately 10 minutes), congratulations! You will easily obtain validation for the claims listed in the [Introduction](#introduction).

- **Precision and Recall**  (Section 6.2 of our paper)

  The bytecode you input in the GUI will be stored in the 'input_bytecode' file, and the analysis results will be saved in the 'output_VaTy. txt' file. In order to facilitate inspection, we have extracted all variables from the contract file and placed them in the '`/VarLifter/source code of test cases/ground-truth_&_ouput/n_ground_truth.txt`' file as the ground truth. You can obtain some metrics of the analysis results (including precision, recall, and time) by running the `get_precision_recall.py` script. For convenience, we have already run it in advance and present the results in the following table, which can be used directly for reference.







| contract         | #1   | #2   | #3   | #4   | #5   | #6   | #7   | #8   | #9   | #10  | #11  | #12  | #13  | #14  | #15  | Av.      |
| ---------------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | -------- |
| **TP**           | 27   | 24   | 23   | 17   | 13   | 19   | 36   | 7    | 19   | 12   | 23   | 11   | 8    | 2    | 4    | \        |
| **TP+FP**        | 27   | 26   | 23   | 20   | 15   | 19   | 36   | 7    | 24   | 12   | 26   | 12   | 8    | 2    | 4    | \        |
| **TP+FN**        | 27   | 26   | 23   | 20   | 15   | 19   | 36   | 7    | 24   | 12   | 26   | 12   | 8    | 2    | 4    | \        |
| **Precision(%)** | 100  | 92.3 | 100  | 85   | 86.7 | 100  | 100  | 100  | 79.2 | 100  | 88.5 | 91.7 | 100  | 100  | 100  | **94.9** |
| **Recall(%)**    | 100  | 92.3 | 100  | 85   | 86.7 | 100  | 100  | 100  | 79.2 | 100  | 88.5 | 91.7 | 100  | 100  | 100  | **94.9** |

- **Generality and Efficiency**  (Sections 6.3 and 6.4 of our paper)

In terms of generality, the contracts in the small dataset include 10 different compiler versions (declared at the head of the source code), with contract sizes ranging from a minimum of 1KB to a maximum of 32KB (most real-world contract sizes are below 20KB, and contracts with a size of 20KB are considered large). Based on the table above, the performance of VarLifter is not affected by different settings (compiler version, contract size).

In terms of efficiency, the analysis time is printed on the last line of the output. Among these 15 analyses, the shortest time was 0.04 seconds, the longest was 283 seconds, the median is 4.53 seconds, and the average time was 38 seconds. There are more large contracts with sizes above 20KB (4 out of 15) in the test set, if these 4 large contracts are excluded, the average time is 2.8 seconds. 

-  **Advantage** (Section 6.5 of our paper)

  We compared VarLifter with the state-of-the-art decompilers Elipmoc (https://app.dedaub.com/ethereum) and Panoramix (https://etherscan.io/bytecode-decompiler). For the test suite, to save time, we have taken screenshots of their outputs for preservation (see '**../VarLifter/the results of the decompiler used for comparison on the test suite/**'), which you can directly use for verification. We calculated that the precision and recall of Elipmoc are 37% and 34%, respectively, while the precision and recall of Panoramix are 43% and 40%, respectively. It will significantly improve the quality of the results, if we directly replace the variable sections of the existing decompiler outputs with VarLifter's output.

For the results reproduced badge, it is important to note that fully reproducing the experimental results from the paper is a time-consuming and labor-intensive process. Here, we do not claim to fully reproduce the data, but the evaluation results here should reach the level claimed in the paper.

# Reusability Guide

## VarLifter in the package

We have packaged VarLifter, and you can use it as an interface by installing it:

```
cd dist
pip install VarLifter-1.0.0.tar.gz
```

VarLifter's input, core functionality, and output reside in `input_bytecode`,`run_VarLifter.py`, and `output_VaTy.txt`, respectively. You can adapt these files to handle new inputs or customize for specific use cases. Although we try to make VarLifter as easy to reuse as possible, the following points still need to be noted:

- The core artifact is designed to work in a specific Python environment with certain dependencies. Users need to ensure they replicate the exact environment to avoid compatibility issues. Using tools like virtualenv or conda can help manage the environment effectively.

- The artifact relies on several libraries and packages. Any updates or changes in these dependencies might affect the functionality. It's recommended to use a requirements.txt file to manage these dependencies and ensure consistency.
- The artifact has been primarily tested on Linux-based systems. While it should theoretically work on Windows and MacOS, there might be platform-specific issues that haven't been addressed. Users on Windows and MacOS may need to make additional modifications or troubleshoot compatibility issues.
- Setting up the artifact might require a moderate level of technical expertise, particularly in configuring the environment and dependencies. Detailed setup instructions are provided, but users should be comfortable with command-line operations and Python programming.

- VarLifter is specifically designed to work with Solidity bytecode. Its reusability is limited to projects that involve Ethereum smart contracts written in Solidity.

## Other functionalities

- Some components of VarLifter may also have standalone value, such as bytecode disassembly. You can save the bytecode you want to disassemble in the `input_bytecode` file, then execute the `disassembler.py` script. You will see the disassembly results in the `disassembly_result.txt` file.

- VarLifter also outputs information on which state variables are read or written by functions, as well as the local variables within functions (stored in the stack without storage slot numbers). This information is provided for potential research purposes and is not within the scope of this paper.

## **Limitations to the artifact's reusability**

- Documentation Coverage: While the provided documentation covers the core functionality, there might be advanced use cases or edge cases that are not fully documented. Users may need to refer to the source code or seek community support for such scenarios.

- Maintenance and Updates: As the artifact evolves, maintaining backward compatibility might not always be feasible. Users should be prepared for potential breaking changes in future updates and plan accordingly. By following the instructions provided and being aware of these limitations, users can effectively utilize and potentially adapt the core artifact for their specific needs.


##  Troubleshooting

- You may get the exceptions such as '*Unknown opcode*' and '*Stack is empty or index is out of range*'. This is because the compiler is constantly evolving and optimizing. For example, the instruction previously used for hash calculation was 'SHA3', but it has now been changed to 'KECCAK256'. VarLifter is also actively adapting to these changes (we will continue to maintain VarLifter). If you encounter such an exception, please check for any opcode names in the `disassembly_result.txt` file that might not be accounted for.
- For further assistance or questions, please contact the developers.

