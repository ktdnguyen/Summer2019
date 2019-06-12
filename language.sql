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

select *, (sum(speakercount) from languageinfo where 
 from languageinfo
group by language;

