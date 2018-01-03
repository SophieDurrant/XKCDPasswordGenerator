# XKCD Style Password Generator

## Sypnosis

This script generates programs in the style recommended by https://www.xkcd.com/936/.

This also includes features to specify word count, password length, and the inclusion of capital letters, special characters, and digits.

## Code Example

```
~$ ./XKCDPasswordGenerator.py 
opennesstongasignupwool

~$ ./XKCDPasswordGenerator.py --number-of-words 7
josephinechatfreshmenseniorvoipjanuarykeyword

~$ ./XKCDPasswordGenerator.py --capitalize 0.3 --special-number 0.3 --special-character 0.3
poland7euro~pdb3greenville=0
```

## Installation

Program runs as a standalone script.

1. Download XKCDPasswordGenerator.py and 20k.txt into same directory
1. From directory run `python3 XKCDPasswordGenerator.py`

## Acknowledgements

Many thanks to the contributors of https://github.com/first20hours/google-10000-english for supplying the 20k English word list.

Many thanks to Randall Munroe of xkcd.com for the inspiration.

## License

Source code is licensed with the BSD 2-Clause license.