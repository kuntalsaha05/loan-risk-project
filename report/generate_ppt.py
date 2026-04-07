from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.util import Inches, Pt


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
VISUALS_DIR = BASE_DIR / "visuals"
OUTPUT_PATH = BASE_DIR / "Loan_Risk_Project_Presentation.pptx"


def add_title_slide(prs: Presentation, title: str, subtitle: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    slide.placeholders[1].text = subtitle


def add_bullet_slide(prs: Presentation, title: str, bullets: list[str]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    text_frame = slide.placeholders[1].text_frame
    text_frame.clear()

    first = True
    for bullet in bullets:
        p = text_frame.paragraphs[0] if first else text_frame.add_paragraph()
        p.text = bullet
        p.level = 0
        p.font.size = Pt(22)
        first = False


def add_table_slide(prs: Presentation, title: str, columns: list[str], rows: list[list[str]]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = title
    table = slide.shapes.add_table(
        rows=len(rows) + 1,
        cols=len(columns),
        left=Inches(0.5),
        top=Inches(1.5),
        width=Inches(9),
        height=Inches(4.5),
    ).table

    for col_index, column in enumerate(columns):
        table.cell(0, col_index).text = column

    for row_index, row in enumerate(rows, start=1):
        for col_index, value in enumerate(row):
            table.cell(row_index, col_index).text = value


def add_image_slide(prs: Presentation, title: str, image_name: str, caption: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = title
    image_path = VISUALS_DIR / image_name
    if image_path.exists():
        slide.shapes.add_picture(str(image_path), Inches(0.7), Inches(1.5), width=Inches(8.6))
    tx_box = slide.shapes.add_textbox(Inches(0.7), Inches(6.5), Inches(8.5), Inches(0.5))
    tx_box.text_frame.text = caption


def add_architecture_slide(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Architecture Flow"
    steps = [
        "Dataset",
        "Preprocessing",
        "ETL",
        "Warehouse",
        "Association Mining",
        "Classification",
        "Clustering",
        "Visualization",
        "System Output",
    ]
    left = 0.5
    top = 2.0
    width = 1.0
    height = 0.7

    for index, step in enumerate(steps):
        shape = slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
            Inches(left + (index % 3) * 3.0),
            Inches(top + (index // 3) * 1.3),
            Inches(2.2),
            Inches(height),
        )
        shape.text_frame.text = step


def build_presentation() -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    add_title_slide(
        prs,
        "Loan Risk Analysis and Prediction System",
        "DET Mini Project Presentation",
    )

    add_bullet_slide(
        prs,
        "Project Objective",
        [
            "Analyze a real loan dataset and identify default-related patterns",
            "Apply preprocessing, ETL, association mining, classification, and clustering",
            "Present insights using charts, reports, and a prediction module",
        ],
    )

    add_bullet_slide(
        prs,
        "Dataset Exploration",
        [
            "Dataset: lending_club_loan_two.csv",
            "Rows: 396,030 and selected features: 24",
            "Explored numerical, categorical, and time-related fields",
            "Key risk indicators: loan amount, income, DTI, loan status, grade",
        ],
    )

    add_bullet_slide(
        prs,
        "Data Preprocessing",
        [
            "Handled missing values and removed unnecessary columns",
            "Clipped outliers using IQR-based limits",
            "Transformed date fields into issue year, issue month, and credit history years",
            "Created engineered features: default_flag and default_stage",
        ],
    )

    add_bullet_slide(
        prs,
        "Unit III Concepts and Algorithm",
        [
            "Association rule mining finds relationships among borrower features",
            "Support measures frequency, confidence measures reliability, and lift measures strength",
            "Apriori algorithm was used after converting continuous values into buckets",
        ],
    )

    add_bullet_slide(
        prs,
        "Unit IV Concepts and Algorithms",
        [
            "Supervised learning predicts default using labeled data",
            "Unsupervised learning groups borrowers without target labels",
            "Algorithms used: Logistic Regression, Decision Tree, Random Forest, and K-Means",
        ],
    )

    add_table_slide(
        prs,
        "Supervised Learning Results",
        ["Model", "Accuracy", "F1 Score"],
        [
            ["Logistic Regression", "0.8056", "0.0876"],
            ["Decision Tree", "0.8017", "0.1476"],
            ["Random Forest", "0.8047", "0.0358"],
        ],
    )

    add_table_slide(
        prs,
        "Unsupervised Learning Results",
        ["Cluster", "Records", "Default Rate"],
        [
            ["low_risk", "41,823", "0.1199"],
            ["medium_risk", "29,702", "0.1893"],
            ["high_risk", "48,475", "0.2673"],
        ],
    )

    add_bullet_slide(
        prs,
        "Visualization Tools and Techniques",
        [
            "Tools used: Python, Matplotlib, and Seaborn",
            "Charts created: risk distribution, cluster scatter plot, association rules, and model comparison",
            "Visualizations support analysis, reporting, and presentation clarity",
        ],
    )

    add_image_slide(prs, "Risk Distribution", "risk_distribution.png", "Borrower status distribution from the processed dataset")
    add_image_slide(prs, "Cluster Visualization", "cluster_scatter.png", "K-Means borrower clusters by income and DTI")
    add_image_slide(prs, "Association Rules", "association_rules.png", "Top association rules ranked by confidence")

    add_bullet_slide(
        prs,
        "System Implementation",
        [
            "Built a prediction module for default probability estimation",
            "Added stage classification, interest recommendation, and what-if simulation",
            "Demo output: default probability 0.081, non_default stage, low_risk cluster",
        ],
    )

    add_architecture_slide(prs)

    add_bullet_slide(
        prs,
        "Conclusion",
        [
            "The project covers DET syllabus Units I-IV in one workflow",
            "It combines preprocessing, ETL, association mining, ML models, clustering, and visualization",
            "The final system demonstrates practical loan risk prediction and analysis",
        ],
    )

    return prs


def main() -> None:
    prs = build_presentation()
    try:
        prs.save(str(OUTPUT_PATH))
        print(f"Presentation created at: {OUTPUT_PATH}")
    except PermissionError:
        fallback_path = OUTPUT_PATH.with_name("Loan_Risk_Project_Presentation_Updated.pptx")
        prs.save(str(fallback_path))
        print(f"Presentation created at: {fallback_path}")


if __name__ == "__main__":
    main()
