import yaml
from pathlib import Path
from datetime import datetime

# 数据库配置
DB_USER = "postgres"
DB_PASSWORD = "nasa718"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "test_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 会议信息 NeurIPS 2024
START_DATE = datetime(2024, 12, 10)
END_DATE = datetime(2024, 12, 15)
LOCATION = "Vancouver, Canada"
WEBSITE = "https://neurips.cc/virtual/2024/index.html"
CATEGORY = "machine learning, neuroscience, statistics, optimization, computer vision, natural language processing, life sciences, natural sciences, social sciences"
DESCRIPTION = "The Conference and Workshop on Neural Information Processing Systems is a machine learning and computational neuroscience conference held every December. Along with ICLR and ICML, it is one of the three primary conferences of high impact in machine learning and artificial intelligence research."


# 追踪机构名单
def load_organization_config() -> dict:
    """Load organization configuration from YAML file."""
    config_path = Path(__file__).parent / "organizations.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

# Load the configuration
ORG_CONFIG = load_organization_config()
# Create list of all tracked organizations
TRACKED_ORGANIZATIONS = [
    org["name"]
    for organizations in ORG_CONFIG["tracked_organizations"].values()
    for org in organizations
]