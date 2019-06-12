select * from countrylanguage;

#
#table of distinct languages
#
drop table languagecountry;
create table languagecountry as
select d.language
from countrylanguage as d, country as e
#where e.Code = (select d.CountryCode)
group by d.language
order by language;


select * from languagecountry;

#
#count of distinct languages
#
select count(language) as DistinctLanguages
from languagecountry;

###
#
#table Q1.2
#
#
###
drop table LanguageInfo;
create table LanguageInfo as
(
	select a.Code, a.Population, b.CountryCode, b.Language, b.Percentage
    from country as a
	left join countrylanguage as b on b.CountryCode=a.Code
) 

order by CountryCode;

#
#calculate the number of people who speak that language in that country
#
alter table languageinfo
#drop column speakercount;
add SpeakerCount int;
#languageinfo.population*languageinfo.percentage;
;
#
#calculate number of speakers
#
update languageinfo
set speakercount = (population*percentage)/100
where (percentage>0 and population>0);


select * from country;

select * from languageinfo;

#
#table with distinct languages and total speakers of each language
#
drop table totallanguage;
create table totallanguage as
select language,
	sum(speakercount) as TotalSpeaker
from languageinfo group by language
order by totalspeaker desc
;

select * from totallanguage;

drop table top10language;
create table top10language as
select language
from totallanguage
limit 10;

select * from top10language;


##
#
#
#	Q2
#
#
##

#total number of countries
select count(code) as CountryCount
from country;


##
# country that speaks less popular language
##


select 
	(
    select count(a.code) as LessPopularLanguageCountry
	from languageinfo as a, top10language as b
	where a.language = b.language and a.percentage > 50
    )
    / count(code) as Fraction_of_Countries_Speaking_less_popular_languages
    from country
    ;





#
#
#
# 2
#
#
#

select a.ID as CityCode, a.name as CityName, a.population as CityPopulation, 
b.district as DistrictName, b.districtpop as DistrictPopulation, b.cityCount as CityCount_District,
b.countrycode as CountryCode,
c.name as CountryName, c.population as CountryPopulation
from city as a 
 join district as b
 join country as c
	on c.code = b.countrycode
    and a.countrycode = c.code;
