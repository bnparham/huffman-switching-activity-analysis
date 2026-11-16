
import heapq
import itertools
from collections import Counter

import pandas as pd

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt


# ============================================================
# 1. HUFFMAN CODING
# ============================================================

def build_huffman_code(frequencies):

    heap = []
    counter = itertools.count()

    for symbol, freq in sorted(frequencies.items()):
        heapq.heappush(
            heap,
            (freq, next(counter), {symbol: ""})
        )

    if len(heap) == 1:
        symbol = next(iter(frequencies))
        return {symbol: "0"}

    while len(heap) > 1:

        freq1, _, codes1 = heapq.heappop(heap)
        freq2, _, codes2 = heapq.heappop(heap)

        merged = {}

        for symbol, code in codes1.items():
            merged[symbol] = "0" + code

        for symbol, code in codes2.items():
            merged[symbol] = "1" + code

        heapq.heappush(
            heap,
            (freq1 + freq2, next(counter), merged)
        )

    return heap[0][2]


# ============================================================
# 2. TRANSITION COUNTER
# ============================================================

def count_transitions(binary_string):

    return sum(
        binary_string[i] != binary_string[i - 1]
        for i in range(1, len(binary_string))
    )


# ============================================================
# 3. GENERATE ALL 2-BIT FULL ADDER RESULTS
# ============================================================

rows = []

for a in range(4):

    for b in range(4):

        result = a + b

        binary_result = format(result, "03b")

        rows.append({

            "Input A (Decimal)": a,
            "Input A (Binary)": format(a, "02b"),

            "Input B (Decimal)": b,
            "Input B (Binary)": format(b, "02b"),

            "Result (Decimal)": result,
            "Result (Binary)": binary_result,

            # Transitions inside this result only
            "Original Transitions":
                count_transitions(binary_result)

        })


# ============================================================
# 4. RESULT FREQUENCIES
# ============================================================

results = [row["Result (Decimal)"] for row in rows]

frequencies = Counter(results)

huffman_codes = build_huffman_code(frequencies)


# ============================================================
# 5. HUFFMAN ENCODING AND ROW-BY-ROW ANALYSIS
# ============================================================

for row in rows:

    result = row["Result (Decimal)"]

    code = huffman_codes[result]

    row["Huffman Code"] = code

    row["Huffman Length"] = len(code)

    # Transitions inside this Huffman codeword only
    row["Huffman Transitions"] = count_transitions(code)


# ============================================================
# 6. CREATE ORIGINAL AND COMPRESSED BITSTREAMS
# ============================================================

original_stream = "".join(
    row["Result (Binary)"] for row in rows
)

huffman_stream = "".join(
    row["Huffman Code"] for row in rows
)


# ============================================================
# 7. TOTAL TRANSMISSION METRICS
# ============================================================

original_length = len(original_stream)
huffman_length = len(huffman_stream)

original_total_transitions = count_transitions(original_stream)
huffman_total_transitions = count_transitions(huffman_stream)

# Transition density = transitions / total adjacent-bit positions

original_density = (
    original_total_transitions / (original_length - 1)
)

huffman_density = (
    huffman_total_transitions / (huffman_length - 1)
)

compression_saving = (
    (original_length - huffman_length) / original_length * 100
)


# ============================================================
# 8. ROW-BY-ROW REPORT
# ============================================================

df = pd.DataFrame(rows)

print("\n========== ROW-BY-ROW RESULTS ==========\n")

print(df.to_string(index=False))


# ============================================================
# 9. FREQUENCY REPORT
# ============================================================

frequency_rows = []

for result in sorted(frequencies):

    frequency_rows.append({

        "Decimal Result": result,

        "Binary Result": format(result, "03b"),

        "Frequency": frequencies[result],

        "Huffman Code": huffman_codes[result],

        "Huffman Code Length": len(huffman_codes[result])

    })

frequency_df = pd.DataFrame(frequency_rows)

print("\n========== RESULT FREQUENCIES ==========\n")

print(frequency_df.to_string(index=False))


# ============================================================
# 10. TOTAL TRANSMISSION COMPARISON
# ============================================================

comparison_df = pd.DataFrame([

    {

        "Method": "Original",

        "Total Bits": original_length,

        "Total Transitions": original_total_transitions,

        "Transition Density (%)": original_density * 100

    },

    {

        "Method": "Huffman",

        "Total Bits": huffman_length,

        "Total Transitions": huffman_total_transitions,

        "Transition Density (%)": huffman_density * 100

    }

])

print("\n========== TRANSMISSION COMPARISON ==========\n")

print(comparison_df.to_string(index=False))


print("\n========== FINAL METRICS ==========\n")

print(f"Original transmission length: {original_length} bits")

print(f"Huffman transmission length: {huffman_length} bits")

print(f"Compression saving: {compression_saving:.2f}%")

print(f"Original total transitions: {original_total_transitions}")

print(f"Huffman total transitions: {huffman_total_transitions}")

print(f"Original transition density: {original_density * 100:.2f}%")

print(f"Huffman transition density: {huffman_density * 100:.2f}%")


# ============================================================
# 11. BITSTREAM REPORT
# ============================================================

print("\n========== BITSTREAMS ==========\n")

print("Original:")
print(original_stream)

print("\nHuffman:")
print(huffman_stream)


# ============================================================
# 12. EXCEL EXPORT
# ============================================================

with pd.ExcelWriter("full_adder_huffman_report.xlsx") as writer:

    df.to_excel(
        writer,
        sheet_name="Row Analysis",
        index=False
    )

    frequency_df.to_excel(
        writer,
        sheet_name="Frequencies",
        index=False
    )

    comparison_df.to_excel(
        writer,
        sheet_name="Comparison",
        index=False
    )

    pd.DataFrame([

        {
            "Method": "Original",
            "Bitstream": original_stream
        },

        {
            "Method": "Huffman",
            "Bitstream": huffman_stream
        }

    ]).to_excel(
        writer,
        sheet_name="Bitstreams",
        index=False
    )


# ============================================================
# 13. IMAGE REPORT
# ============================================================

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# ------------------------------------------------------------
# Prepare report data
# ------------------------------------------------------------

comparison_df = pd.DataFrame({
    "Method": ["Original", "Huffman"],
    "Total Bits": [original_length, huffman_length],
    "Total Transitions": [
        original_total_transitions,
        huffman_total_transitions
    ],
    "Transition Density (%)": [
        original_density * 100,
        huffman_density * 100
    ]
})

metrics_df = pd.DataFrame({
    "Metric": [
        "Original Bitstream Length",
        "Huffman Bitstream Length",
        "Compression Saving",
        "Original Total Transitions",
        "Huffman Total Transitions",
        "Original Transition Density",
        "Huffman Transition Density"
    ],
    "Value": [
        f"{original_length} bits",
        f"{huffman_length} bits",
        f"{compression_saving:.2f}%",
        original_total_transitions,
        huffman_total_transitions,
        f"{original_density * 100:.2f}%",
        f"{huffman_density * 100:.2f}%"
    ]
})


# ------------------------------------------------------------
# Create figure layout
# ------------------------------------------------------------

fig = plt.figure(figsize=(18, 25))

gs = GridSpec(
    5, 2,
    figure=fig,
    height_ratios=[1.2, 1.2, 1.3, 1.5, 1.5],
    hspace=0.65,
    wspace=0.3
)

fig.suptitle(
    "2-Bit Full Adder: Original vs Huffman",
    fontsize=20,
    fontweight="bold",
    y=0.99
)


# ============================================================
# ROW 1: ORIGINAL CHARTS
# ============================================================

# ------------------------------------------------------------
# 1. Result frequencies
# ------------------------------------------------------------

ax1 = fig.add_subplot(gs[0, 0])

ax1.bar(
    frequency_df["Decimal Result"].astype(str),
    frequency_df["Frequency"]
)

ax1.set_title(
    "Frequency of Each Result",
    fontsize=13
)

ax1.set_xlabel("Decimal Result")
ax1.set_ylabel("Frequency")
ax1.grid(axis="y", alpha=0.3)


# ------------------------------------------------------------
# 2. Transitions per result
# ------------------------------------------------------------

ax2 = fig.add_subplot(gs[0, 1])

x = range(len(df))

ax2.plot(
    x,
    df["Original Transitions"],
    marker="o",
    label="Original"
)

ax2.plot(
    x,
    df["Huffman Transitions"],
    marker="s",
    label="Huffman"
)

ax2.set_title(
    "Transitions Per Result",
    fontsize=13
)

ax2.set_xlabel("Operation Index")
ax2.set_ylabel("Transitions")
ax2.legend()
ax2.grid(alpha=0.3)


# ============================================================
# ROW 2: ORIGINAL CHARTS
# ============================================================

# ------------------------------------------------------------
# 3. Total transmission bits
# ------------------------------------------------------------

ax3 = fig.add_subplot(gs[1, 0])

ax3.bar(
    ["Original", "Huffman"],
    [original_length, huffman_length]
)

ax3.set_title(
    "Total Transmission Length",
    fontsize=13
)

ax3.set_ylabel("Number of Bits")
ax3.grid(axis="y", alpha=0.3)


# ------------------------------------------------------------
# 4. Overall transition density
# ------------------------------------------------------------

ax4 = fig.add_subplot(gs[1, 1])

ax4.bar(
    ["Original", "Huffman"],
    [
        original_density * 100,
        huffman_density * 100
    ]
)

ax4.set_title(
    "Overall Transition Density",
    fontsize=13
)

ax4.set_ylabel("Transition Density (%)")
ax4.grid(axis="y", alpha=0.3)


# ============================================================
# ROW 3: RESULT FREQUENCY AND HUFFMAN TABLE
# ============================================================

ax5 = fig.add_subplot(gs[2, :])
ax5.axis("off")

frequency_report = frequency_df[
    [
        "Decimal Result",
        "Binary Result",
        "Frequency",
        "Huffman Code",
        "Huffman Code Length"
    ]
]

frequency_table = ax5.table(
    cellText=frequency_report.values,
    colLabels=frequency_report.columns,
    cellLoc="center",
    loc="center"
)

frequency_table.auto_set_font_size(False)
frequency_table.set_fontsize(10)
frequency_table.scale(1, 1.8)

ax5.set_title(
    "Result Frequency and Huffman Codes",
    fontsize=14,
    fontweight="bold",
    pad=20
)


# ============================================================
# ROW 4: TRANSMISSION COMPARISON AND FINAL METRICS
# ============================================================

# ------------------------------------------------------------
# 5. Transmission comparison table
# ------------------------------------------------------------

ax6 = fig.add_subplot(gs[3, 0])
ax6.axis("off")

comparison_table = ax6.table(
    cellText=comparison_df.values,
    colLabels=comparison_df.columns,
    cellLoc="center",
    loc="center"
)

comparison_table.auto_set_font_size(False)
comparison_table.set_fontsize(9)
comparison_table.scale(1, 2)

ax6.set_title(
    "Transmission Comparison",
    fontsize=14,
    fontweight="bold",
    pad=20
)


# ------------------------------------------------------------
# 6. Final metrics table
# ------------------------------------------------------------

ax7 = fig.add_subplot(gs[3, 1])
ax7.axis("off")

metrics_table = ax7.table(
    cellText=metrics_df.values,
    colLabels=metrics_df.columns,
    cellLoc="center",
    loc="center"
)

metrics_table.auto_set_font_size(False)
metrics_table.set_fontsize(9)
metrics_table.scale(1, 1.8)

ax7.set_title(
    "Final Metrics",
    fontsize=14,
    fontweight="bold",
    pad=20
)


# ============================================================
# ROW 5: COMPLETE BITSTREAMS
# ============================================================

# ------------------------------------------------------------
# 7. Original bitstream
# ------------------------------------------------------------

ax8 = fig.add_subplot(gs[4, 0])
ax8.axis("off")

ax8.set_title(
    f"Original Bitstream ({original_length} bits)",
    fontsize=13,
    fontweight="bold",
    pad=15
)

ax8.text(
    0.02,
    0.95,
    original_stream,
    fontsize=9,
    family="monospace",
    verticalalignment="top",
    wrap=True,
    transform=ax8.transAxes
)


# ------------------------------------------------------------
# 8. Huffman bitstream
# ------------------------------------------------------------

ax9 = fig.add_subplot(gs[4, 1])
ax9.axis("off")

ax9.set_title(
    f"Huffman Bitstream ({huffman_length} bits)",
    fontsize=13,
    fontweight="bold",
    pad=15
)

ax9.text(
    0.02,
    0.95,
    huffman_stream,
    fontsize=9,
    family="monospace",
    verticalalignment="top",
    wrap=True,
    transform=ax9.transAxes
)


# # ============================================================
# # SAVE IMAGE
# # ============================================================

plt.savefig(
    "full_adder_huffman_report.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Image report saved: full_adder_huffman_report.png")


# ============================================================
# 14. MULTI-STREAM SWITCHING ACTIVITY EXPERIMENT
# ============================================================

import random
import textwrap
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# ------------------------------------------------------------
# 1. EXPERIMENT CONFIGURATION
# ------------------------------------------------------------

RANDOM_SEED = 2026
NUMBER_OF_RANDOM_STREAMS = 5
STREAM_LENGTH = 16

rng = random.Random(RANDOM_SEED)


# ------------------------------------------------------------
# 2. USE THE EXISTING HUFFMAN CODEBOOK
# ------------------------------------------------------------

# The codebook is built from the original full-adder frequencies.
# The same codebook is reused for every stream.

huffman_codebook = {
    int(row["Decimal Result"]): str(row["Huffman Code"])
    for _, row in frequency_df.iterrows()
}

# Original full-adder output sequence
original_sequence = [
    int(value) for value in df["Result (Decimal)"]
]

# Validate the original sequence
assert len(original_sequence) == STREAM_LENGTH

# Validate the codebook
assert set(huffman_codebook.keys()) == set(range(7))


# ------------------------------------------------------------
# 3. GENERATE FIVE RANDOM STREAMS
# ------------------------------------------------------------

streams = {
    "Original": original_sequence
}

for i in range(1, NUMBER_OF_RANDOM_STREAMS + 1):

    random_sequence = [
        rng.randint(0, 6)
        for _ in range(STREAM_LENGTH)
    ]

    streams[f"Random {i}"] = random_sequence


# ------------------------------------------------------------
# 4. ENCODING FUNCTIONS
# ------------------------------------------------------------

def original_encode(sequence):

    return [
        format(value, "03b")
        for value in sequence
    ]


def huffman_encode(sequence):

    return [
        huffman_codebook[value]
        for value in sequence
    ]


# ------------------------------------------------------------
# 5. TRANSITION COUNTING FUNCTIONS
# ------------------------------------------------------------

def count_intra_transitions(codewords):

    """
    Count transitions inside each individual codeword.
    """

    transitions = []

    for word in codewords:

        count = sum(
            word[i] != word[i + 1]
            for i in range(len(word) - 1)
        )

        transitions.append(int(count))

    return transitions


def count_inter_transitions(codewords):

    """
    Count transitions between consecutive codewords.

    Example:
        110 | 001

        Last bit of first word = 0
        First bit of second word = 0

        Boundary transitions = 0
    """

    transitions = []

    for i in range(len(codewords) - 1):

        last_bit = codewords[i][-1]
        first_bit = codewords[i + 1][0]

        transitions.append(
            int(last_bit != first_bit)
        )

    return transitions


def analyze_encoding(codewords):

    """
    Analyze one encoded stream.
    """

    intra = count_intra_transitions(codewords)

    inter = count_inter_transitions(codewords)

    total_intra = sum(intra)
    total_inter = sum(inter)

    total_transitions = total_intra + total_inter

    bitstream = "".join(codewords)

    total_bits = len(bitstream)

    transition_density = (
        total_transitions / (total_bits - 1) * 100
        if total_bits > 1
        else 0
    )

    return {
        "Codewords": codewords,
        "Bitstream": bitstream,
        "Total Bits": total_bits,
        "Intra Transitions": total_intra,
        "Inter Transitions": total_inter,
        "Total Transitions": total_transitions,
        "Transition Density (%)": transition_density,
        "Intra Per Word": intra,
        "Inter Per Boundary": inter
    }


# ------------------------------------------------------------
# 6. ANALYZE ALL STREAMS
# ------------------------------------------------------------

all_results = {}

metrics_records = []
comparison_records = []

for stream_name, sequence in streams.items():

    # Original fixed-length encoding
    original_words = original_encode(sequence)

    original_analysis = analyze_encoding(original_words)

    # Huffman encoding
    huffman_words = huffman_encode(sequence)

    huffman_analysis = analyze_encoding(huffman_words)

    all_results[stream_name] = {
        "Decimal Sequence": sequence,
        "Original": original_analysis,
        "Huffman": huffman_analysis
    }

    # Save individual metrics
    for method, analysis in [
        ("Original", original_analysis),
        ("Huffman", huffman_analysis)
    ]:

        metrics_records.append({
            "Stream": stream_name,
            "Method": method,
            "Total Bits": analysis["Total Bits"],
            "Intra Transitions": analysis["Intra Transitions"],
            "Inter Transitions": analysis["Inter Transitions"],
            "Total Transitions": analysis["Total Transitions"],
            "Transition Density (%)":
                analysis["Transition Density (%)"]
        })

    # Compare both methods for this stream
    original_bits = original_analysis["Total Bits"]
    huffman_bits = huffman_analysis["Total Bits"]

    compression_saving = (
        (original_bits - huffman_bits) / original_bits * 100
    )

    transition_difference = (
        original_analysis["Total Transitions"]
        - huffman_analysis["Total Transitions"]
    )

    comparison_records.append({
        "Stream": stream_name,
        "Original Bits": original_bits,
        "Huffman Bits": huffman_bits,
        "Compression Saving (%)": compression_saving,
        "Original Transitions":
            original_analysis["Total Transitions"],
        "Huffman Transitions":
            huffman_analysis["Total Transitions"],
        "Transition Reduction":
            transition_difference
    })


# ------------------------------------------------------------
# 7. CREATE DATAFRAMES
# ------------------------------------------------------------

metrics_df_multi = pd.DataFrame(metrics_records)

comparison_df_multi = pd.DataFrame(comparison_records)


# ============================================================
# 8. PRINT EXPERIMENTAL RESULTS
# ============================================================

print("\n" + "=" * 75)
print("MULTI-STREAM SWITCHING ACTIVITY EXPERIMENT")
print("=" * 75)

for stream_name, result in all_results.items():

    print(f"\n\n{stream_name}")
    print("-" * 75)

    print("Decimal sequence:")
    print(result["Decimal Sequence"])

    for method in ["Original", "Huffman"]:

        analysis = result[method]

        print(f"\n{method} encoding:")

        print("Codewords:")
        print(" | ".join(analysis["Codewords"]))

        print("Bitstream:")
        print(analysis["Bitstream"])

        print("Intra transitions per word:")
        print(analysis["Intra Per Word"])

        print("Inter transitions per boundary:")
        print(analysis["Inter Per Boundary"])

        print("Total bits:", analysis["Total Bits"])
        print("Intra transitions:", analysis["Intra Transitions"])
        print("Inter transitions:", analysis["Inter Transitions"])
        print("Total transitions:", analysis["Total Transitions"])

        print(
            "Transition density:",
            f"{analysis['Transition Density (%)']:.2f}%"
        )


print("\n\n" + "=" * 75)
print("OVERALL COMPARISON")
print("=" * 75)

print(comparison_df_multi.to_string(index=False))


# ============================================================
# 9. GENERATE SEPARATE IMAGE REPORT
# ============================================================

fig = plt.figure(figsize=(23, 36))

gs = GridSpec(
    5, 2,
    figure=fig,
    height_ratios=[1, 1, 1, 1.5, 1.3],
    hspace=0.65,
    wspace=0.25
)

fig.suptitle(
    "Multi-Stream Encoding and Switching Activity Analysis",
    fontsize=21,
    fontweight="bold",
    y=0.995
)

codebook_text = " | ".join(
    f"{value}: {huffman_codebook[value]}"
    for value in sorted(huffman_codebook)
)

fig.text(
    0.5,
    0.978,
    f"Huffman Codebook (trained on original stream): {codebook_text}",
    ha="center",
    fontsize=10
)


# ------------------------------------------------------------
# 10. DISPLAY ALL SIX STREAMS
# ------------------------------------------------------------

for index, (stream_name, result) in enumerate(all_results.items()):

    row = index // 2
    col = index % 2

    ax = fig.add_subplot(gs[row, col])
    ax.axis("off")

    original = result["Original"]
    huffman = result["Huffman"]

    decimal_text = " ".join(
        str(value) for value in result["Decimal Sequence"]
    )

    original_words = " | ".join(original["Codewords"])
    huffman_words = " | ".join(huffman["Codewords"])

    original_intra = original["Intra Per Word"]
    original_inter = original["Inter Per Boundary"]

    huffman_intra = huffman["Intra Per Word"]
    huffman_inter = huffman["Inter Per Boundary"]

    content = (
        f"DECIMAL SEQUENCE:\n"
        f"{textwrap.fill(decimal_text, width=65)}\n\n"

        f"ORIGINAL ENCODING ({original['Total Bits']} bits):\n"
        f"{textwrap.fill(original_words, width=65)}\n\n"

        f"HUFFMAN ENCODING ({huffman['Total Bits']} bits):\n"
        f"{textwrap.fill(huffman_words, width=65)}\n\n"

        f"ORIGINAL - INTRA TRANSITIONS PER WORD:\n"
        f"{original_intra}\n\n"

        f"ORIGINAL - INTER TRANSITIONS PER BOUNDARY:\n"
        f"{original_inter}\n\n"

        f"HUFFMAN - INTRA TRANSITIONS PER WORD:\n"
        f"{huffman_intra}\n\n"

        f"HUFFMAN - INTER TRANSITIONS PER BOUNDARY:\n"
        f"{huffman_inter}"
    )

    ax.text(
        0.02,
        0.96,
        content,
        fontsize=8.5,
        family="monospace",
        verticalalignment="top",
        transform=ax.transAxes
    )

    ax.set_title(
        stream_name,
        fontsize=14,
        fontweight="bold",
        pad=12
    )

    for spine in ax.spines.values():
        spine.set_visible(True)


# ------------------------------------------------------------
# 11. OVERALL METRICS TABLE
# ------------------------------------------------------------

ax_metrics = fig.add_subplot(gs[3, :])
ax_metrics.axis("off")

metrics_display = metrics_df_multi.copy()

metrics_display["Transition Density (%)"] = (
    metrics_display["Transition Density (%)"].map(
        lambda x: f"{x:.2f}%"
    )
)

metrics_table = ax_metrics.table(
    cellText=metrics_display.values,
    colLabels=metrics_display.columns,
    cellLoc="center",
    loc="center"
)

metrics_table.auto_set_font_size(False)
metrics_table.set_fontsize(9)
metrics_table.scale(1, 1.8)

ax_metrics.set_title(
    "Switching Activity: Detailed Metrics for All Streams",
    fontsize=15,
    fontweight="bold",
    pad=20
)


# ------------------------------------------------------------
# 12. COMPRESSION AND TRANSITION COMPARISON TABLE
# ------------------------------------------------------------

ax_comparison = fig.add_subplot(gs[4, :])
ax_comparison.axis("off")

comparison_display = comparison_df_multi.copy()

comparison_display["Compression Saving (%)"] = (
    comparison_display["Compression Saving (%)"].map(
        lambda x: f"{x:.2f}%"
    )
)

comparison_table = ax_comparison.table(
    cellText=comparison_display.values,
    colLabels=comparison_display.columns,
    cellLoc="center",
    loc="center"
)

comparison_table.auto_set_font_size(False)
comparison_table.set_fontsize(9)
comparison_table.scale(1, 1.8)

ax_comparison.set_title(
    "Original vs Huffman: Compression and Transition Comparison",
    fontsize=15,
    fontweight="bold",
    pad=20
)


# ------------------------------------------------------------
# 13. SAVE IMAGE
# ------------------------------------------------------------


plt.savefig(
    "multi_stream_switching_activity_report.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "\nReport saved: "
    "multi_stream_switching_activity_report.png"
)