Feature: css3-fonts
 Scenario: font matching rule 001
   When launch "css3-fonts-app"
     And I go to "csswg/font-matching-rule-001.htm"
     And I save the page to "font-matching-rule-001"
    Then pic "font-matching-rule-001" of baseline and result should be "100" similar if have results
