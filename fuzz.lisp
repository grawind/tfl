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

(defparameter *rule-t2*
  '(("cc" "aa")
    ("aba" "a")
    ("abc" "aa")
    ("bba" "aca")
    ("acb" "abb")
    ("baa" "aa")
    ("aaa" "bb")
    ("caa" "aa")
    ("cbb" "cba")
    ("cbc" "c")
    ("bb" "aa")
    ("ac" "aa")
    ("cba" "aa")
    ("aab" "aa")))

(defparameter *size-rule-t* 14)
(defparameter *size-rule-t2* 12) 

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
        (when (null pos) (return positions))
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

(defparameter *viewed-words* nil)

(defun dfs (s s-1)
  (when (string= s s-1)
    (return-from dfs t))
  
  (dolist (rule *rule-t2*)
    (let ((positions (find-overlaps s (first rule))))
      (when positions
        (dolist (p positions)
          (let ((s2 (apply-the-rule s rule p)))
            (unless (member s2 *viewed-words* :test #'string=)
              (push s2 *viewed-words*)
              (when (string= s2 s-1)
                (return-from dfs t))
              (when (dfs s2 s-1)
                (return-from dfs t))))))))
  nil)

(defun main ()
  (let ((fl t))
    (dotimes (j 100)
      (let* ((ss (random-string 10))
             (t-seq (random-sequence-rule 20))
             (s-0 ss))
        (dolist (i t-seq)
          (let* ((rule (nth i *rule-t*))
                 (positions (find-overlaps ss (first rule)))
                 (k (length positions)))
            (when (> k 0)
              (setf ss (apply-the-rule ss 
                                      rule 
                                      (nth (random k) positions))))))
        (let ((s-1 ss))
          (setf *viewed-words* nil)
          (unless (dfs s-0 s-1)
            (format t "Не удалось найти путь:~%")
            (format t "s_0: ~A~%" s-0)
            (format t "s_1: ~A~%" s-1)
            (setf fl nil)))))
    (when fl
      (format t "True~%"))))


(main)