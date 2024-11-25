import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.package_price_agent_tool import PackagePriceAgentTool

def test_package_price_agent():
    package_tool = PackagePriceAgentTool(excel_path='./data/vivecolombia.xlsx')
    response = package_tool._run(country='colombia-ejemplo', city='cartagena', currency='dolares')
    print(response)

if __name__ == "__main__":
    test_package_price_agent()
