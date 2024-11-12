# Findings

## 1. Results

<!-- _In this subsection, you should report the results from your experiments in a summary table, keeping only the most relevant results for your experiment (ie your best model, and two or three other options which you explored). You should also briefly explain the summary table and highlight key results._ -->

### 1.1 Classification Model Results

<div align="center">

<table style="border-collapse: collapse; width: 100%;">
    <thead>
        <tr>
            <th style="border: 1px solid lightgrey; padding: 8px;"></th>
            <th style="border: 1px solid lightgrey; padding: 8px;">Ridge</th>
            <th style="border: 1px solid lightgrey; padding: 8px;">Ridge 5k</th>
            <th style="border: 1px solid lightgrey; padding: 8px;">XGBoost</th>
            <th style="border: 1px solid lightgrey; padding: 8px;">DistilBERT old</th>
            <th style="border: 1px solid lightgrey; padding: 8px;">DistilBERT 5k</th>
            <th style="border: 1px solid lightgrey; padding: 8px;">DistilBERT</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="border: 1px solid lightgrey; padding: 8px;">No Hate/Toxic</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.67</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.61</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.65</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.45</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.63</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.72</td>
        </tr>
        <tr>
            <td style="border: 1px solid lightgrey; padding: 8px;">Toxic 1</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.57</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.54</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.52</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.21</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.36</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.61</td>
        </tr>
        <tr>
            <td style="border: 1px solid lightgrey; padding: 8px;">Toxic 2</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.78</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.40</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.42</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.34</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.39</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.79</td>
        </tr>
        <tr>
            <td style="border: 1px solid lightgrey; padding: 8px;">Toxic 3</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.99</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.60</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.68</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.08</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.98</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.98</td>
        </tr>
        <tr>
            <td style="border: 1px solid lightgrey; padding: 8px;">Hate 1</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.74</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.70</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.73</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.40</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.77</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.79</td>
        </tr>
        <tr>
            <td style="border: 1px solid lightgrey; padding: 8px;">Hate 2</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.97</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.87</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.91</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.60</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.94</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.97</td>
        </tr>
        <tr>
            <td style="border: 1px solid lightgrey; padding: 8px;">Hate 3</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.99</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.99</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.94</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.57</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.99</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">0.99</td>
        </tr>
        <tr>
            <td style="border: 1px solid lightgrey; padding: 8px;"><b>Macro Avg F1-score</b></td>
            <td style="border: 1px solid lightgrey; padding: 8px;"><b>0.81</b></td>
            <td style="border: 1px solid lightgrey; padding: 8px;"><b>0.72</b></td>
            <td style="border: 1px solid lightgrey; padding: 8px;"><b>0.81</b></td>
            <td style="border: 1px solid lightgrey; padding: 8px;"><b>0.39</b></td>
            <td style="border: 1px solid lightgrey; padding: 8px;"><b>0.72</b></td>
            <td style="border: 1px solid lightgrey; padding: 8px;"><b>0.84</b></td>
        </tr>
    </tbody>
</table>

</div>

<div align="center" style="font-size:  0.85em;">

Table 3: Model Experimentation Results comparing macro-average F1-scores between different classifier models. Model names with "5k" indicate that the model was trained on a smaller dataset containing less synthetic data that we generated to balance the classes. DistilBERT old was trained on data labelled with a previous version of class defintions that made classes less distinct from each other.

</div>

DistilBERT achieved the highest F1-score (0.84), making it the top-performing model. Models trained on the smaller 5k dataset (a mix of synthetic and actual labelled data), and in certain synthetically generated classes showed lower F1-scores, indicating that the reduced dataset may lack the nuanced variations found in real-world text, which are crucial for effective hate and toxic speech detection. DistilBERT old, trained with previous class definitions, had the lowest macro-average F1-score (0.39), underscoring the importance of the updated, distinct class definitions in improving classification accuracy.

## 2. Discussion

_In this subsection, you should discuss what the results mean for the business user – specifically how the technical metrics translate into business value and costs, and whether this has sufficiently addressed the business problem._

_You should also discuss or highlight other important issues like interpretability, fairness, and deployability._

## 3. Recommendations

_In this subsection, you should highlight your recommendations for what to do next. For most projects, what to do next is either to deploy the model into production or to close off this project and move on to something else. Reasoning about this involves understanding the business value, and the potential IT costs of deploying and integrating the model._

_Other things you can recommend would typically relate to data quality and availability, or other areas of experimentation that you did not have time or resources to do this time round._
