
# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# Function to print success messages in green
echo_success() {
  echo -e "${GREEN}$1${NC}"
}

# Function to print warning messages in yellow
echo_warning() {
  echo -e "${YELLOW}$1${NC}"
}

# Function to print error messages in red
echo_error() {
  echo -e "${RED}$1${NC}"
}

# Function to print info messages in cyan
echo_info() {
  echo -e "${CYAN}$1${NC}"
}

# Function to print general messages in blue
echo_blue() {
  echo -e "${BLUE}$1${NC}"
}
