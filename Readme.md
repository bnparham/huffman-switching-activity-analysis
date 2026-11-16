# Huffman Encoding & Switching Activity Analysis

An experimental study of the relationship between data compression and switching activity in digital systems, comparing conventional fixed-length binary encoding with Huffman variable-length encoding.

## 1. Motivation

Dynamic power consumption in digital circuits is influenced by signal switching activity. Data encoding techniques can change both the length and transition patterns of transmitted bitstreams.

Although Huffman coding can reduce the number of transmitted bits, a shorter bitstream does not necessarily result in fewer bit transitions.

This project investigates that relationship using a 2-bit full adder as the data source.

## 2. Objectives

- Compare fixed-length binary encoding and Huffman encoding.
- Measure intra-codeword and inter-codeword bit transitions.
- Evaluate total transmission length and transition density.
- Investigate the relationship between compression efficiency and switching activity.
- Compare results across the original full-adder sequence and five random sequences.

## 3. Methodology

The experiment generates all 16 input combinations of a 2-bit full adder. Its decimal outputs range from 0 to 6 and are represented using 3-bit binary encoding.

A Huffman codebook is constructed using the original output frequencies and reused for all six experimental sequences.

The analysis considers the following metrics:

| Metric             | Description                                                 |
| ------------------ | ----------------------------------------------------------- |
| Total Bits         | Encoded bitstream length                                    |
| Compression Saving | Reduction in bitstream length                               |
| Intra Transitions  | Transitions within codewords                                |
| Inter Transitions  | Transitions between consecutive codewords                   |
| Total Transitions  | Sum of intra- and inter-codeword transitions                |
| Transition Density | Percentage of adjacent-bit positions containing transitions |

### Evaluation Formulas

Total transitions:

$$T_{\text{total}} = T_{\text{intra}} + T_{\text{inter}}$$

Transition density:

$$D_{\text{transition}} = \frac{T_{\text{total}}}{L-1} \times 100$$

Compression saving:

$$S = \frac{L_{\text{original}}-L_{\text{Huffman}}}{L_{\text{original}}} \times 100$$

where \(L\) is the total bitstream length.

## 4. Experimental Reports

The project automatically generates two separate visual reports:

### Original Full-Adder Analysis

`full_adder_huffman_report.png`

Includes:

- Output frequency distribution.
- Transitions per full-adder result.
- Total transmission length.
- Overall transition density.
- Huffman codebook and frequency table.
- Transmission comparison and final metrics.
- Complete original and Huffman bitstreams.

### Multi-Stream Analysis

`multi_stream_switching_activity_report.png`

Includes:

- One original and five random decimal sequences.
- Original and Huffman codewords for every sequence.
- Intra- and inter-codeword transition counts.
- Detailed switching activity metrics.
- Compression and transition comparisons.

### Excel Results

`full_adder_huffman_report.xlsx`

Contains structured experimental results, frequency information, encoding comparisons, and complete bitstreams.

## 5. My Contributions

- Designed the experimental setup using a 2-bit full adder.
- Implemented Huffman coding and codebook generation.
- Developed bitstream construction and transition-counting mechanisms.
- Extended the analysis to multiple reproducible random sequences.
- Evaluated compression efficiency and switching activity using quantitative metrics.
- Implemented automated visualization and Excel reporting using Python.

## 6. Technologies

Python · Pandas · Matplotlib · Huffman Coding · Data Analysis

## 7. Limitations and Future Work

Transition count is used as an indicator of switching activity, not as a direct measurement of power consumption.

Future work can include parallel-bus switching analysis using Hamming distance, FPGA implementation, and actual energy measurements that account for encoding and decoding overhead.

## 8. Conclusion

This experiment demonstrates why compression efficiency and switching activity should be evaluated separately. Reducing the number of transmitted bits does not necessarily reduce bit transitions, highlighting an important consideration when investigating encoding techniques for low-power digital systems.
