/*
 * Facts about the weather.  May be used as test data for Assignment 4.
 * Students: do NOT add your rules to this file!  Put your rules in a separate
 * file and hand in just that file.  
 * CISC 260, Winter 2018
 * M. Lamb
 */
 
% weather facts have 5 parameters:
%   1. a month (the usual 3-letter abbreviations, all lower case)
%   2. a day (an integer between 1 and 31)
%   3-5. three atoms describing the weather on this day.  The atoms
%        must contain one of (cold, cool, warm, hot) to describe
%        the temperature, one of (rain, snow, dry) to describe
%        precipitation if any, and one of (wind, calm) to tell if
%        there was much wind.  These three atoms may occur in any
%        order but must come after the month and the day.

% The following facts were generated at random.  They don't correspond
% to any actual weather data.  
weather(jan, 17, cold, wind, snow).
weather(feb, 7, rain, warm, calm).
weather(apr, 1, cool, wind, dry).
weather(apr, 3, wind, warm, rain).
weather(apr, 4, dry, calm, warm).
weather(apr, 16, wind, cold, snow).
weather(apr, 20, cool, rain, wind).
weather(apr, 24, wind, snow, cold).
weather(apr, 27, dry, calm, cool).
weather(may, 23, warm, snow, calm).
weather(may, 26, dry, cool, calm).
weather(jun, 20, snow, wind, cold).
weather(jul, 18, hot, rain, calm).
weather(jul, 20, hot, dry, calm).
weather(sep, 15, calm, dry, cool).
weather(sep, 16, rain, hot, calm).
weather(sep, 18, warm, rain, calm).
weather(oct, 29, cool, dry, calm).
weather(nov, 1, cold, snow, wind).
weather(nov, 5, hot, snow, wind).
weather(dec, 15, warm, rain, wind).
weather(dec, 21, wind, cold, dry).
