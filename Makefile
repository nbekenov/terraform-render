
help:
	@echo make targets:
	@awk ' \
	    BEGIN { FS=":.*?## " } \
	    $$1~/^[A-Za-z]/ && $$2~/^.+/ { \
	        printf "    * %-18.18s %s\n",$$1":",$$2 \
	    }' $(MAKEFILE_LIST)

all: clean install lint build test

install: ## install python packages
	@printf "\n\n\033[0;32m** Installing dependencies **\n\n\033[0m"
	pipenv install
	pipenv install --dev

# ===== CODE LEVEL
#

lint:  ## check syntax of python code
	@printf "\n\n\033[0;32m** Checking Python code for syntax errors (fatal) **\n\n\033[0m"
	pipenv run pylint --errors-only tests/*.py
	@echo "###############################"
	@printf "\n\n\033[0;32m** Checking Python code for syntax suggestions (non-fatal) **\n\n\033[0m"
	pipenv run pylint --exit-zero tests/*.py


test: ## run pytest
	@printf "\n\n\033[0;32m** Unit testing (pytest) **\n\n\033[0m"
	pipenv run pytest -s -vvv tests/	


# ===== PROJECT LEVEL
#
build: ## generate terraform plan
	@printf "\n\n\033[0;32m** Generating terraform plan **\n\n\033[0m"
	for case in complete-mssql complete-postgres complete-oracle ; do \
		echo $$case ; \
		cd testcases/$$case && terraform init ; \
		terraform plan -out terraform.plan ; \
		terraform show -json terraform.plan > plan.json ; \
		pipenv run python -m json.tool plan.json > plan_formated.json ; \
		cd ../.. ; \
	done

clean: ## delete pytest_cache and generated terraform files
	rm -rf .pytest_cache
	rm -rf testcases/complete-mssql/.terraform
	rm -rf testcases/complete-mssql/.terraform.lock.hcl
	rm -rf testcases/complete-mssql/plan.json
	rm -rf testcases/complete-mssql/plan_formated.json
	rm -rf testcases/complete-mssql/terraform.plan
	rm -rf testcases/complete-postgres/.terraform
	rm -rf testcases/complete-postgres/.terraform.lock.hcl
	rm -rf testcases/complete-postgres/plan.json
	rm -rf testcases/complete-postgres/plan_formated.json
	rm -rf testcases/complete-postgres/terraform.plan
	rm -rf testcases/complete-oracle/.terraform
	rm -rf testcases/complete-oracle/.terraform.lock.hcl
	rm -rf testcases/complete-oracle/plan.json
	rm -rf testcases/complete-oracle/plan_formated.json
	rm -rf testcases/complete-oracle/terraform.plan

check: ## check versions
	terraform --version
	pipenv run python --version