(defparameter *alphabet* "abc")
(defparameter *size-alphabet* 3)


(defparameter *rule-t*
  '(("cc" "aa")
    ("aaa" "aa")
    ("ababaabcba" "aaba")
    ("aacb" "aa")
    ("aabc" "aa")
    ("aba" "a")
    ("abc" "aa")
    ("abba" "aca")
    ("acb" "abb")
    ("baa" "aa")
    ("aaaba" "bb")
    ("caa" "aa")
    ("caca" "cba")
    ("cbc" "c")))

(defparameter *size-rule-t* 14)

(defun random-string (n)
  (let ((result (make-string n)))
    (dotimes (i n result)
      (setf (char result i)
            (char *alphabet* (random *size-alphabet*))))))

(defun random-sequence-rule (n)
  (loop for i from 0 below n
        collect (random *size-rule-t*)))

(defun find-overlaps (s sub)
  (let ((positions '())
        (start 0)
        (sub-len (length sub)))
    (loop
      (let ((pos (search sub s :start2 start)))
        (when (null pos) (return (reverse positions)))
        (push pos positions)
        (setf start (1+ pos))))))

(defun apply-the-rule (s rule position)
  (let* ((rule-from (first rule))
         (rule-to (second rule))
         (before (subseq s 0 position))
         (after (subseq s position)))
    (concatenate 'string 
                 before 
                 (substitute rule-to rule-from after :count 1))))

(defun matrix-equal (m1 m2)
  (and (equal (first m1) (first m2))
       (equal (second m1) (second m2))))

(defun calculations-in-matrix-form (s)
  (if (string= s "")
      '((0 0) (0 0))
      (let ((result nil))
        (case (char s 0)
          (#\a (setf result '((0 0) (0 0))))
          (#\b (setf result '((0 1) (0 0))))
          (#\c (setf result '((0 0) (1 0)))))
        
        (loop for i from 1 below (length s) do
          (case (char s i)
            (#\a (setf result '((0 0) (0 0))))  
            (#\b (setf result `((0 ,(first (first result)))  
                                (0 ,(first (second result))))))
            (#\c (setf result `((,(second (first result)) 0)  
                                (,(second (second result)) 0))))))
        result)))

(defun multiplication-in-Z4 (s)
  (let ((result 1))
    (loop for char across s do
      (case char
        (#\a (setf result 0))  ; a = 0
        (#\b (setf result (mod (* result 2) 4)))  ; b = 2
        (#\c (setf result 0))))  ; c = 0
    result))
    
(defun test-invariant-Z4 (s0 s1)
  (= (multiplication-in-Z4 s0) (multiplication-in-Z4 s1)))

(defun test-invariant (s0 s1)
  (matrix-equal (calculations-in-matrix-form s0)
                (calculations-in-matrix-form s1)))

(defun main ()
  (let ((fl t))
    (dotimes (j 50000)
      (let ((ss (random-string 10))
            (t-seq (random-sequence-rule 20))
            (s-0 ""))
        (setf s-0 ss)
        
        (dolist (i t-seq)
          (let* ((rule (nth i *rule-t*))
                 (positions (find-overlaps ss (first rule)))
                 (k (length positions)))
            (when (> k 0)
              (setf ss (apply-the-rule ss 
                                      rule 
                                      (nth (random k) positions))))))
        
        (let ((s-1 ss))
          (unless (and (test-invariant s-0 s-1)
                       (test-invariant-Z4 s-0 s-1))
            (format t "Инвариант нарушен:~%")
            (format t "s_0: ~A~%" s-0)
            (format t "s_1: ~A~%" s-1)
            (format t "Матрица s_0: ~A~%" (calculations-in-matrix-form s-0))
            (format t "Матрица s_1: ~A~%" (calculations-in-matrix-form s-1))
            (format t "Z4 s_0: ~A~%" (multiplication-in-Z4 s-0))
            (format t "Z4 s_1: ~A~%" (multiplication-in-Z4 s-1))
            (setf fl nil)))))
    
    (if fl
        (format t "True~%")
        (format t "False~%"))))

(main)
