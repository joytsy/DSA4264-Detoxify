---
updated: 4 October 2024
authors:
  - Richmond Sin
---

# Classes, Types, and All

This page is a overview on how objects should be documented.

A special syntax should be adhered to when labeling objects, attributes, etc. within documentation to improve readability. These special labels are called `doculabels`.

    @​label(<label>)

!!! WARNING "Zero width space character"

    To prevent any of the strings in this document from being redered as a `doculabel`, a zero space character was placed into the string. Do not copy the code in any of the blocks.

The following labels can be used, simply type any of the texts below into the rounded brackets (and remove the angled brackets).

- @label(class)
- @label(pipe)
- @label(service)
- @label(interface)
- @label(type)
- @label(attr)
- @label(meth)
- @label(func)
- @label(private)
- @label(read only)
- @label(deprecated)

While they can be rendered anywhere on the page, they should only be used in header elements (H2 and below).

---

## Page Layout

Objects/types/interfaces/etc. should always have the second highest hierarchy, and should never be the highest. Page titles (`#` H1 tags) should be reserved purely for the name of the page.

All objects and attributes (including private, read only, deprecated) should be documented.

Below is a very rough example of how a page should be written.

=== "Markdown"

    ```
    ## @​label(class) MyExampleClass

    Short description of my class.

    ### Attributes

    #### @​label(attr) codeAttributeName
    `attrTypr` and explain what this attribute is for

    ### Methods

    #### @​label(meth) My Humanised Method Name

        ```
        myMethodName(arg0:type):type
        ```

    Description
    : Some verbose reason what this method is for.

    Parameters
    : `arg0` (`type`): Description of `arg0` and its relation to the method.

    Returns
    : `type` and its significance.
    ```

Generally speaking, the following patterns can be followed.

- Descriptive sections (e.g. attributes, methods, specific method groups) should be `H3`.
- Actual code attributes, methods, and all should be `H4`.

!!! NOTE

    See the example below for a visual example of how a page should look like.

---

## Attributes​

All attributes must be labeled, with their respective types. To mark additional `doculabels`, they must be done in this order.

1. @label(deprecated)
2. @label(private)
3. @label(read only)
4. @label(attr)

=== "Markdown"

    ```
    #### @​label(attr) myAttribute
    `type` example to show attribute

    #### @​label(private) @​label(attr) youShouldntUseThisOutside
    `type` an example private attribute
    ```

---

## Methods and Functions

Methods can be grouped together under the same `H3` header if they have similar relations.

=== "Markdown"

    ```
    ### Methods related to Apples

    #### @​label(meth) Create apple
    ...

    #### @​label(meth) Delete apple
    ...

    ### Methods related to Oranges

    #### @​label(meth) Create orange
    ...

    #### @​label(meth) Delete orange
    ...

    ```

For each method or function, the following items must be documented for clarity.

1. Call signature
2. Description
3. Parameters
4. Return type

### Call Signature

This should be documented in a code block in the language the piece of code was written in. If it was written in TypeScript, it should look like this.

    async function createApple(apple:Apple):Promise<string>

### Description

A short sentence should be added to give a very summarised brief on what the function or method should do.

=== "Markdown"

    ```
    Description
    : Creates an apple in the fruit basket.
    ```

### Parameters

For each of the parameters, the name, type, and description of it should be given.

The syntax should look like this.

    Parameter
    : `nameOfParam1` (`type`): Description
    : `nameOfParam2` (`type`): Description

=== "Markdown"

    ```
    Parameters
    : `apple` (`Apple`): Creates the `Apple` fruit that should be added to the basket.
    ```

### Returns

This is particularly important as it outlines what the return type is, and its significance.

=== "Markdown"

    ```
    Returns
    : `string` Id of the apple created
    ```

---

## @label(class) ExampleFruitBasket

This is an example of how a rendered class would look like

### Attributes

#### @label(attr) fruits

`Fruit[]` an array containing all the fruits in the basket.

### Methods related to apples

#### @label(meth) Add apple

    addApple(apple:Apple):void

Description
: Adds an apple to the fruit basket.

Parameters
: `apple` (`Apple`): Apple to be added

Returns
: `void`

### Methods related to oranges

#### @label(meth) Add Orange

    addOrange(orange:Orange):void

Description
: Adds an orange to the fruit basket.

Parameters
: `orange` (`Orange`): Orange to be added

Returns
: `void`

#### @label(meth) Eat Orange by Id

    async eatOrange(id:string, round:boolean):Promise<number>

Description
: Eat and orange and count the number of bites.

Parameters
: `id` (`string`): UUID of the `Orange` to be eaten.
: `round` (`boolean`): Specifies if the `Orange` must be round.

Returns
: `number` of bites needed to finish eating the orange
