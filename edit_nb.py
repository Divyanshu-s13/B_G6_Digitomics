import nbformat

nb_path = '/Users/soumyatiwari/Desktop/B_G6_Digitomics/notebooks/02_cleaning.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

new_markdown_source = """### 5.4 Engineer academic_risk_score

The `academic_risk_score` column originally contains only 0.0 values.
It is recalculated using a relevant weighted formula based on other columns:
`(100 - class_attendance_rate) * 0.4 + (10 - academic_motivation) * 2.5 + (digital_addiction_score) * 0.5 + (brain_rot_index) * 0.3`
The score is then clipped at 0 to prevent negative values."""

new_code_source = """df["academic_risk_score"] = (
    (100 - df["class_attendance_rate"]) * 0.4 +
    (10 - df["academic_motivation"]) * 2.5 +
    df["digital_addiction_score"] * 0.5 +
    df["brain_rot_index"] * 0.3
)

# Ensure no negative scores
df["academic_risk_score"] = df["academic_risk_score"].clip(lower=0)

print("academic_risk_score summary after engineering:")
print(df["academic_risk_score"].describe())"""

new_md_cell = nbformat.v4.new_markdown_cell(new_markdown_source)
new_code_cell = nbformat.v4.new_code_cell(new_code_source)

insert_idx = -1
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'markdown' and '## 6. Round Float' in cell.source:
        insert_idx = i
        break

if insert_idx != -1:
    nb.cells.insert(insert_idx, new_code_cell)
    nb.cells.insert(insert_idx, new_md_cell)

# Update summary cell
for cell in nb.cells:
    if cell.cell_type == 'markdown' and '## Summary' in cell.source:
        lines = cell.source.split('\n')
        for i, line in enumerate(lines):
            if '- Encoded binary categoricals' in line:
                lines.insert(i, "- **Added**: `academic_risk_score` engineered using a weighted formula based on class attendance, motivation, digital addiction, and brain rot.")
                break
        cell.source = '\n'.join(lines)

with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Updated notebook successfully!")
