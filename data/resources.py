"""
Learning Resources Database - Curated resources mapped by topic and level.
Each resource has: title, type, url, level, description
"""

RESOURCES = {
    "Machine Learning Basics": [
        {
            "title": "Introduction to Machine Learning",
            "type": "video",
            "url": "https://www.youtube.com/watch?v=ukzFI9rgwfU",
            "level": "Beginner",
            "description": "Crash course on what ML is, types of ML, and real-world applications.",
            "icon": "▶️",
        },
        {
            "title": "Machine Learning Crash Course by Google",
            "type": "course",
            "url": "https://developers.google.com/machine-learning/crash-course",
            "level": "Beginner",
            "description": "Google's free, fast-paced ML course with TensorFlow exercises.",
            "icon": "📚",
        },
        {
            "title": "Extra Practice Quiz: ML Basics",
            "type": "quiz",
            "url": "/quiz/Machine%20Learning%20Basics",
            "level": "Beginner",
            "description": "Practice fundamental ML concepts with adaptive quiz questions.",
            "icon": "🧪",
        },
        {
            "title": "ML Cheatsheet",
            "type": "article",
            "url": "https://ml-cheatsheet.readthedocs.io/en/latest/",
            "level": "All",
            "description": "Quick-reference glossary of core ML concepts and algorithms.",
            "icon": "📝",
        },
        {
            "title": "Hands-On Machine Learning (Aurélien Géron)",
            "type": "book",
            "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/",
            "level": "Intermediate",
            "description": "The definitive practical guide to ML with Scikit-Learn and TensorFlow.",
            "icon": "📖",
        },
    ],

    "Linear Regression": [
        {
            "title": "Linear Regression Basics",
            "type": "video",
            "url": "https://www.youtube.com/watch?v=nk2CQITm_eo",
            "level": "Beginner",
            "description": "Beginner-friendly walkthrough of slope, intercept, and line fitting.",
            "icon": "▶️",
        },
        {
            "title": "Linear Regression Explained - StatQuest",
            "type": "video",
            "url": "https://www.youtube.com/watch?v=7ArmBVF2dCs",
            "level": "Beginner",
            "description": "Clear visual explanation of linear regression from scratch.",
            "icon": "▶️",
        },
        {
            "title": "Linear Regression Practice - Kaggle",
            "type": "exercise",
            "url": "https://www.kaggle.com/learn/intro-to-machine-learning",
            "level": "Beginner",
            "description": "Hands-on linear regression exercises on real datasets.",
            "icon": "💻",
        },
        {
            "title": "Regression Analysis Complete Guide",
            "type": "article",
            "url": "https://towardsdatascience.com/linear-regression-detailed-view-ea73175f6e86",
            "level": "Intermediate",
            "description": "In-depth coverage of assumptions, diagnostics, and multiple regression.",
            "icon": "📝",
        },
    ],

    "Classification": [
        {
            "title": "Logistic Regression - StatQuest",
            "type": "video",
            "url": "https://www.youtube.com/watch?v=yIYKR4sgzI8",
            "level": "Beginner",
            "description": "Visual walkthrough of logistic regression and sigmoid function.",
            "icon": "▶️",
        },
        {
            "title": "Classification in ML - Towards Data Science",
            "type": "article",
            "url": "https://towardsdatascience.com/machine-learning-classifiers-a5cc4e1b0623",
            "level": "Beginner",
            "description": "Overview of common classification algorithms with code examples.",
            "icon": "📝",
        },
        {
            "title": "Classification on Kaggle",
            "type": "exercise",
            "url": "https://www.kaggle.com/competitions/titanic",
            "level": "Intermediate",
            "description": "Classic Titanic survival classification challenge — perfect for practice.",
            "icon": "💻",
        },
    ],

    "Probability & Statistics": [
        {
            "title": "Statistics and Probability - Khan Academy",
            "type": "course",
            "url": "https://www.khanacademy.org/math/statistics-probability",
            "level": "Beginner",
            "description": "Free, comprehensive statistics course from fundamentals to inference.",
            "icon": "📚",
        },
        {
            "title": "Bayes Theorem - 3Blue1Brown",
            "type": "video",
            "url": "https://www.youtube.com/watch?v=HZGCoVF3YvM",
            "level": "Beginner",
            "description": "Beautiful visual explanation of Bayes' theorem.",
            "icon": "▶️",
        },
        {
            "title": "Think Stats (Free Book)",
            "type": "book",
            "url": "https://greenteapress.com/thinkstats2/html/index.html",
            "level": "Intermediate",
            "description": "Statistics for programmers — uses Python examples throughout.",
            "icon": "📖",
        },
    ],

    "Linear Algebra": [
        {
            "title": "Essence of Linear Algebra - 3Blue1Brown",
            "type": "video",
            "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab",
            "level": "Beginner",
            "description": "The most beautiful visual introduction to linear algebra ever made.",
            "icon": "▶️",
        },
        {
            "title": "Linear Algebra for ML - Fast.ai",
            "type": "course",
            "url": "https://www.fast.ai/posts/linear-algebra-calculus-deep-learning.html",
            "level": "Intermediate",
            "description": "Practical linear algebra concepts needed specifically for ML.",
            "icon": "📚",
        },
    ],

    "Data Preprocessing": [
        {
            "title": "Data Cleaning Tutorial - Kaggle",
            "type": "course",
            "url": "https://www.kaggle.com/learn/data-cleaning",
            "level": "Beginner",
            "description": "Hands-on data cleaning with Python and Pandas.",
            "icon": "💻",
        },
        {
            "title": "Feature Engineering Guide",
            "type": "article",
            "url": "https://towardsdatascience.com/feature-engineering-for-machine-learning-3a5e293a5114",
            "level": "Intermediate",
            "description": "Comprehensive guide to preprocessing, encoding, and feature creation.",
            "icon": "📝",
        },
    ],

    "Overfitting & Underfitting": [
        {
            "title": "Bias-Variance Tradeoff - StatQuest",
            "type": "video",
            "url": "https://www.youtube.com/watch?v=EuBBz3bI-aA",
            "level": "Beginner",
            "description": "Clear visual explanation of the bias-variance tradeoff.",
            "icon": "▶️",
        },
        {
            "title": "Regularization Explained",
            "type": "article",
            "url": "https://towardsdatascience.com/regularization-in-machine-learning-76441ddcf99a",
            "level": "Intermediate",
            "description": "Complete guide to L1, L2, and Elastic Net regularization.",
            "icon": "📝",
        },
    ],

    "Neural Networks": [
        {
            "title": "Neural Networks - 3Blue1Brown",
            "type": "video",
            "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi",
            "level": "Beginner",
            "description": "Visual series on how neural networks learn — stunning animations.",
            "icon": "▶️",
        },
        {
            "title": "Deep Learning Specialization - Coursera",
            "type": "course",
            "url": "https://www.coursera.org/specializations/deep-learning",
            "level": "Intermediate",
            "description": "Andrew Ng's famous Deep Learning course series.",
            "icon": "📚",
        },
        {
            "title": "Neural Network Playground",
            "type": "exercise",
            "url": "https://playground.tensorflow.org/",
            "level": "Beginner",
            "description": "Interactive visual tool to experiment with neural networks in your browser.",
            "icon": "🎮",
        },
    ],

    "Decision Trees": [
        {
            "title": "Decision Trees - StatQuest",
            "type": "video",
            "url": "https://www.youtube.com/watch?v=7VeUPuFGJHk",
            "level": "Beginner",
            "description": "Step-by-step explanation of how decision trees work.",
            "icon": "▶️",
        },
        {
            "title": "Random Forests - StatQuest",
            "type": "video",
            "url": "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ",
            "level": "Intermediate",
            "description": "How Random Forests improve upon single decision trees.",
            "icon": "▶️",
        },
    ],

    "Clustering": [
        {
            "title": "K-Means Clustering Explained - StatQuest",
            "type": "video",
            "url": "https://www.youtube.com/watch?v=4b5d3muPQmA",
            "level": "Beginner",
            "description": "Visual walkthrough of the K-Means algorithm.",
            "icon": "▶️",
        },
        {
            "title": "Unsupervised Learning - Sklearn",
            "type": "article",
            "url": "https://scikit-learn.org/stable/unsupervised_learning.html",
            "level": "Intermediate",
            "description": "Official Scikit-learn guide to clustering and dimensionality reduction.",
            "icon": "📝",
        },
    ],

    "General": [
        {
            "title": "Kaggle Learn — Free Courses",
            "type": "course",
            "url": "https://www.kaggle.com/learn",
            "level": "All",
            "description": "Free, hands-on ML courses with real datasets and immediate feedback.",
            "icon": "📚",
        },
        {
            "title": "Fast.ai Practical Deep Learning",
            "type": "course",
            "url": "https://course.fast.ai/",
            "level": "Intermediate",
            "description": "Top-down, practical approach to deep learning. Completely free.",
            "icon": "📚",
        },
        {
            "title": "Towards Data Science",
            "type": "blog",
            "url": "https://towardsdatascience.com/",
            "level": "All",
            "description": "Leading publication for data science tutorials and articles.",
            "icon": "📝",
        },
        {
            "title": "Papers With Code",
            "type": "resource",
            "url": "https://paperswithcode.com/",
            "level": "Advanced",
            "description": "Latest ML research papers with open-source implementations.",
            "icon": "🔬",
        },
    ],
}
