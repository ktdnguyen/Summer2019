

# hw1.
#
#	Q1. what are the top 10 most spoken languages?
#	Q2. what fraction of countries in the world speak less-popular languages?
#			# let's say a country "speaks a language" if 50%+ of its population speak that language
			# let's say a less-popular language is any language that is not in the top 10 most spoken


# steps to Q1.
#	1. output a list of distinct languages, and count how many distinct languages there are.
#	2. join country to countrylanguage to create a table with the following fields:
#			CountryCode
#			Language
#			Percentage
# 			CountryPopulation
#	3. to the table you created in (2),
#			- add a column (using alter table)
#			- in this column, calculate the number of people who speak that language in that country
#	4. group the table in (3) over language, to sum the number of people who speak each language
#	5. order the table in (4) in descending order, and limit to 10 to see the top 10 most spoken languages
#	6. make a table, top10language, with the single field, Language, listing the top 10 languages




# steps to Q2.
#	1. count the total number of countries. (denominator)
#	2. calculate the number of countries in the world that speak less-popular languages. (numerator)
#		this is not a straightforward problem. think about it and give it a shot.
#	3. calculate the fraction of countries in the world that speak less-popular languages.




# 2.

# join the three tables into a single table containing the following fields:
#
#		CityCode, 
#		CityName,
#		CityPopulation,
#		DistrictName,
#		DistrictPopulation,
#		CityCount_District,
#		CountryCode,
#		CountryName,
#		CountryPopulation,
#		CityCount_Country











