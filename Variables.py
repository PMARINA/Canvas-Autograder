"""User configuration happens here, also program constants below the line..."""

DOMAIN: str = "abc"  # Your institute's canvas domain (ie abc.instructure.com)

# You don't need to modify anything below this line -----------------------------------------------------------

TOKEN_FILE: str = "Token.pickle"  # The name of the file to use for the user token storage
CONFIG_FILE: str = "Config.pickle"  # The name of the file to use to store user state (for interrupted workflow)


# Constants for use in programs, to ensure consistent key-naming
COURSE_KEY: str = "COURSE"
ASSIGNMENT_KEY: str = "ASSIGNMENT"
SECTION_KEY: str = "SECTION"
